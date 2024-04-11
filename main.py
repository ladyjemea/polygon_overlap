import os
import sys
import time
import argparse
from dotenv import load_dotenv
from pymongo import MongoClient
from shapely.geometry import shape
import shapely.errors


load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]


# Function to detect overlap
def detect_overlap(polygon1, polygon2, threshold):
    try:
        shapely_polygon1 = shape(polygon1)
        shapely_polygon2 = shape(polygon2)

        intersection = shapely_polygon1.intersection(shapely_polygon2)

        intersection_area = intersection.area

        area1 = shapely_polygon1.area
        area2 = shapely_polygon2.area

        overlap_percentage = (intersection_area / min(area1, area2)) * 100

        return overlap_percentage >= threshold
    except shapely.errors.TopologicalError as e:
        print(f"Topological error: {e}. Skipping overlap detection for this pair of polygons.")
        return False
    except Exception as e:
        print(f"Error processing polygons: {e}. Skipping overlap detection for this pair of polygons.")
        return False


def process_polygons(collection_name, geojson_field, overlap_threshold, progress_callback=None):
    collection = db[collection_name]
    polygons = collection.find({}, {geojson_field: 1})
    polygons_list = list(polygons)
    total_polygons = len(polygons_list)
    processed_polygons = 0
    start_time = time.time()

    for i in range(total_polygons):
        for j in range(i + 1, total_polygons):
            polygon1 = polygons_list[i]
            polygon2 = polygons_list[j]

            if detect_overlap(polygon1[geojson_field], polygon2[geojson_field], overlap_threshold):
                print(f"Overlap detected between {polygon1['_id']} and {polygon2['_id']}")

            processed_polygons += 1
            if progress_callback:
                progress_callback(processed_polygons, total_polygons, start_time)

    end_time = time.time()
    print(f"Processed {processed_polygons} polygons in {end_time - start_time:.2f} seconds")


def track_progress(processed_polygons, total_polygons, start_time):
    current_time = time.time()
    elapsed_time = current_time - start_time
    progress_percentage = (processed_polygons / total_polygons) * 100
    sys.stdout.write(f"\rProgress: {processed_polygons}/{total_polygons} polygons processed "
                     f"({progress_percentage:.2f}%), Elapsed Time: {elapsed_time:.2f} seconds")
    sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Polygon Overlap Detection')
    parser.add_argument('collection_name', type=str, help='MongoDB collection name')
    parser.add_argument('geojson_field', type=str, help='Field name containing GeoJSON data')
    parser.add_argument('--overlap_threshold', type=float, default=0.0, help='Minimum overlap percentage threshold')
    parser.add_argument('--track_progress', action='store_true', help='Track and report progress')
    args = parser.parse_args()

    if args.track_progress:
        process_polygons(args.collection_name, args.geojson_field, args.overlap_threshold, track_progress)
    else:
        process_polygons(args.collection_name, args.geojson_field, args.overlap_threshold)
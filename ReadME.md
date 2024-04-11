# Polygon Overlap Detection

This Python script detects overlaps between polygons stored in a MongoDB database. It provides functionalities for dynamic arguments, overlap threshold definition, concurrency, error handling, and progress benchmarking. You need a working MongoDB on your computer with data in it.

## Setup Instructions

1. Clone the repository to your local machine:


2. Install dependencies using pip:


3. Create a `.env` file in the root directory with the following content:


Replace `<your_mongo_host>`, `<your_mongo_port>`, and `<your_mongo_db>` with your MongoDB connection details.

## Running the Script

To run the script, use the command-line instructions:


- `<collection_name>`: MongoDB collection name containing polygons.
- `<geojson_field>`: Field name containing GeoJSON data for polygons.
- `--overlap_threshold <threshold>` (optional): Minimum overlap percentage threshold (default is 0.0).
- `--track_progress` (optional): Track and report progress during execution.


## Understanding Output

The script outputs the detected overlaps between pairs of polygons in the following format:


The IDs `<polygon_id_1>` and `<polygon_id_2>` represent the IDs of the polygons in the MongoDB collection that overlap with each other.

If no overlaps are detected, there will be no output.
import json
from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["polygon_overlap"]  # Replace with your database name
collection = db["overlap"]  # Replace with your collection name

# Load GeoJSON data from a file
with open('p.json', 'r') as file:
    file_data = json.load(file)

def adjust_id_field(document):
    if '_id' in document and '$oid' in document['_id']:
        # Convert $oid to ObjectId
        document['_id'] = ObjectId(document['_id']['$oid'])
    return document

# Adjust _id fields in the loaded data
if isinstance(file_data, list):
    adjusted_data = [adjust_id_field(doc) for doc in file_data]
    for doc in adjusted_data:
        # Check if document with the same _id exists
        if not collection.find_one({'_id': doc['_id']}):
            collection.insert_one(doc)
        else:
            print(f"Document with _id {doc['_id']} already exists in the collection.")
else:
    adjusted_data = adjust_id_field(file_data)
    # Check if document with the same _id exists
    if not collection.find_one({'_id': adjusted_data['_id']}):
        collection.insert_one(adjusted_data)
    else:
        print(f"Document with _id {adjusted_data['_id']} already exists in the collection.")
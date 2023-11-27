import json
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'AT'
collection_name = 'Experimental'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Find documents with "Type": "changed_nodes"
changed_nodes_documents = list(collection.find({'type': 'changed_nodes'}))

# Find documents with "Type": "constant_nodes"
constant_nodes_documents = list(collection.find({'type': 'constant_nodes'}))

# Close the MongoDB connection
client.close()

# Export changed_nodes_documents to a JSON file
with open('image_AT.json', 'w') as changed_nodes_file:
    json.dump(changed_nodes_documents, changed_nodes_file, default=str, indent=2)

# Export constant_nodes_documents to a JSON file
with open('run_AT.json', 'w') as constant_nodes_file:
    json.dump(constant_nodes_documents, constant_nodes_file, default=str, indent=2)

print("Documents exported to JSON files.")

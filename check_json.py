from pymongo import MongoClient
import json

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'AT'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Check if each document is valid JSON
for document in collection.find():
    try:
        json.loads(json.dumps(document, default=str))
        print("Document is valid JSON.")
    except json.JSONDecodeError:
        print("Document is not valid JSON.")

# Close the MongoDB connection
client.close()

import json
from pymongo import MongoClient

def create_summary_json(mongodb_uri, database_name, collection_name, output_file, target_tag):
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Query MongoDB data for the specified tag within children
    cursor = collection.find({"children.tag": target_tag}, {"children.$": 1, "_id": 0})

    # Extract and format data
    summary_data = [{"tag": child["tag"], "text": child["text"]} for doc in cursor for child in doc.get("children", [])]

    # Write to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(summary_data, json_file, indent=2)

    # Close the MongoDB connection
    client.close()

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test_AT'
collection_name = 'collection_AT'
output_file = 'summary.json'

# Specify the target tag for the query
target_tag = 'Focus'

# Call the function to create the summary JSON file for the specified tag within children
create_summary_json(mongodb_uri, database_name, collection_name, output_file, target_tag)

from pymongo import MongoClient
# This script extracts specific combination of information

def extract_information_for_tags(node, tags_to_extract):
    # Extract information from the current node
    tag = node.get('tag', '')
    text = node.get('text', '')

    # Check if the current tag is in the list of tags to extract
    if tag in tags_to_extract:
        print(f"{tag}: {text}")

    # Recursively extract information from child nodes
    for child_node in node.get('children', []):
        extract_information_for_tags(child_node, tags_to_extract)

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'FIBSEM'

# List of tags to extract
tags_to_extract = ['Date', 'Focus']

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Traverse and extract information for specified tags from each document
for document in collection.find():
    print("Extracted Information:")
    extract_information_for_tags(document, tags_to_extract)
    print("\n---\n")

# Close the MongoDB connection
client.close()

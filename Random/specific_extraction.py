from pymongo import MongoClient

# This script extracts specific information
# i.e Given the name of the tag, it spits value under the tag

def extract_information(node):
    # Extract information from the current node
    tag = node.get('tag', '')
    text = node.get('text', '')

    # Print or process the extracted information
    #print(f"Tag: {tag}, Text: {text}")

    # If the tag is "Focus", print its text
    if tag == 'Focus':
        print(f"Focus: {text}")

    # Recursively extract information from child nodes
    for child_node in node.get('children', []):
        extract_information(child_node)


# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'FIBSEM'


# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Traverse and extract information from each document
for document in collection.find():
    print("Extracted Information:")
    extract_information(document)
    print("\n---\n")

# Close the MongoDB connection
client.close()

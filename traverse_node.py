from pymongo import MongoClient

def traverse_document_structure(document, level=0):
    # Print information about the current document
    print(f"{'  ' * level}Node: {document['tag']}")

    # Recursively traverse child nodes
    for child_node in document.get('children', []):
        traverse_document_structure(child_node, level + 1)

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'AT'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Traverse and print the structure of each document
cursor = collection.find()
for document in cursor:
    print("Document Structure:")
    traverse_document_structure(document)
    print("\n---\n")

# Close the MongoDB connection
client.close()

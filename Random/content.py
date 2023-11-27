from pymongo import MongoClient
# Same as extract.py but double check later
def traverse_document_structure(document, level=0):
    # Print information about the current node
    tag = document.get('tag', '')
    text = document.get('text', '')
    print(f"{'  ' * level}{tag} - {text}")

    # Recursively traverse child nodes
    for child_node in document.get('children', []):
        traverse_document_structure(child_node, level + 1)

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'FIBSEM'

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

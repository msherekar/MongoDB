from pymongo import MongoClient

def print_focus_info(document):
    for node in document.get('children', []):
        tag = node.get('tag', '')
        text = node.get('text', '')
        if tag == 'Focus':
            print(f"Tag: {tag}, Text: {text}")

def traverse_document_structure(document, level=0):
    # Print information about the current node
    tag = document.get('tag', '')
    text = document.get('text', '')
    print(f"{'  ' * level}{tag} - {text}")

    # Print focus info if tag is "Focus"
    if tag == 'Focus':
        print_focus_info(document)

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

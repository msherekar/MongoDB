from pymongo import MongoClient

def extract_focus_info(document, focus_info_list):
    # Check if the document has the "Focus" tag
    if "Focus" in document.get("tag", ""):
        # Extract information for the "Focus" tag
        focus_info = {
            "DocumentID": str(document["_id"]),
            "Tag": document.get("tag"),
            "Text": document.get("text"),
            "FocusValue": next((child.get("text") for child in document.get("children", []) if child.get("tag") == "Focus"), None)
        }
        focus_info_list.append(focus_info)

    # Recursively search for the "Focus" tag in children
    for child in document.get("children", []):
        extract_focus_info(child, focus_info_list)

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test_AT'
collection_name = 'collection_AT'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Query all documents in the collection
cursor = collection.find()

# Create a list to store the extracted Focus information
focus_info_list = []

# Traverse documents and extract Focus information
for document in cursor:
    extract_focus_info(document, focus_info_list)

# Print or write the extracted Focus information
print(focus_info_list)

# Close the MongoDB connection
client.close()

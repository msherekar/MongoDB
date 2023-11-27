import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient

# Convert xml to json and then upload json

def parse_xml(element):
    """Recursively parse XML element and convert to JSON-like structure."""
    json_data = {"tag": element.tag, "text": element.text, "children": []}

    for child in element:
        json_data["children"].append(parse_xml(child))

    return json_data

def import_to_mongodb(xml_files_dir, mongodb_uri, database_name, collection_name):
    """Import XML data to MongoDB."""
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Iterate through XML files in the directory
    for filename in os.listdir(xml_files_dir):
        if filename.endswith(".xml"):
            file_path = os.path.join(xml_files_dir, filename)

            # Parse XML
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Convert XML to JSON-like structure
            json_data = parse_xml(root)

            # Insert data into MongoDB collection
            collection.insert_one(json_data)

    # Close the MongoDB connection
    client.close()

# Replace these with your actual values
xml_files_directory = '/Users/mukulsherekar/pythonProject/DatabaseProject/FIBSEM_Files'
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'Experimental'
collection_name = 'FIBSEM'


# Call the function to import data into MongoDB
import_to_mongodb(xml_files_directory, mongodb_uri, database_name, collection_name)

#1. Connect to MongoDB
#2. For each XML file in the directory:
    #a. Parse the XML file
    #b. Convert XML data to a dictionary or JSON-like structure
    #c. Insert the data into MongoDB collection
#3. Close the MongoDB connection

import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient

def parse_xml(file_path):
    """Parse XML file and convert to dictionary."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Convert XML to a dictionary
        xml_data = {
            "root_node": root.tag,
            "data": {}
        }

        for child in root:
            xml_data["data"][child.tag] = child.text

        return xml_data

    except ET.ParseError as e:
        print(f"Error parsing XML file {file_path}: {e}")
        return None

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

            # Parse XML and convert to dictionary
            xml_data = parse_xml(file_path)

            if xml_data:
                # Insert data into MongoDB collection
                collection.insert_one(xml_data)

    # Close the MongoDB connection
    client.close()

# Replace these with your actual values
xml_files_directory = '/Users/mukulsherekar/pythonProject/DatabaseProject/dbprojectxmlfiles'
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test_dict'
collection_name = 'collection_dict'

# Call the function to import data into MongoDB
import_to_mongodb(xml_files_directory, mongodb_uri, database_name, collection_name)


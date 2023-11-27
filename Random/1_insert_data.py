# Strategy: Convert xml to json and then upload json
# This script does the following: Creates a mongoDB, Creates collection within it,
#                                 Reads in the folder of xml, Parses & converts xml to json
#                                 Uploads into mongoDB
# Each folder has collection of xml files coming out of FIBSEM microscope for each experiment (run)
# This Collection of image xmls will become a "Collection" in mongoDB for that experiment
# The location of folder is provided by user (?)
# The script is located in (?)
# Data Model: One Database, One Collections for each experiment (run)
# Duplication check at :

import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient

def parse_xml(element):
    """Recursively parse XML element and convert to JSON-like structure."""
    json_data = {}

    for child in element:
        if len(child) == 0:
            # For leaf nodes, directly assign the text value
            json_data[child.tag] = child.text
        else:
            # For non-leaf nodes, recursively process children
            if child.tag not in json_data:
                json_data[child.tag] = parse_xml(child)

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

# Replace these with your actual names
xml_files_directory = '/Users/mukulsherekar/pythonProject/DatabaseProject/AT_XMLs'
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'AT'
collection_name = 'Experimental'


# Call the function to import data into MongoDB
import_to_mongodb(xml_files_directory, mongodb_uri, database_name, collection_name)

import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient
from tkinter import Tk, filedialog  # For UI file dialog

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
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    for filename in os.listdir(xml_files_dir):
        if filename.endswith(".xml"):
            file_path = os.path.join(xml_files_dir, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()
            json_data = parse_xml(root)
            collection.insert_one(json_data)

    client.close()

def get_user_input_directory():
    """Ask the user to select the XML files directory using a file dialog."""
    root = Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select the XML files directory
    xml_files_directory = filedialog.askdirectory(title="Select XML Files Directory")

    return xml_files_directory

# Replace these with your actual names
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'FIBSEM'

# Uncomment the next line and comment out the line after to use the UI file dialog
xml_files_directory = get_user_input_directory()
#xml_files_directory = '/Users/mukulsherekar/pythonProject/DatabaseProject/FIBSEM_Files'

import_to_mongodb(xml_files_directory, mongodb_uri, database_name, collection_name)

# MongoDB Level Deduplication:
from pymongo import IndexModel, ASCENDING

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Create a unique index on the "unique_identifier" field
index_model = IndexModel([("unique_identifier", ASCENDING)], unique=True)
collection.create_indexes([index_model])

# Close the MongoDB connection
client.close()

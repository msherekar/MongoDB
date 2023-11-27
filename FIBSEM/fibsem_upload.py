# upload_module.py
import os
import xml.etree.ElementTree as ET
from tkinter import filedialog, simpledialog
from pymongo import MongoClient

def get_user_input():
    # change as per user requirements
    folder_path = filedialog.askdirectory(title="Select Folder", initialdir='Users/mukulsherekar/pythonProject/DatabaseProject')
    if not folder_path:
        return None, None, None  # User canceled the operation

    #database_choice = simpledialog.askstring("Select Database", "Choose a database:", initialvalue="")
    database_choice = 'FIBSEM'

    if not database_choice:
        return None, None, None  # User canceled the operation

    collection_name = simpledialog.askstring("Collection Name", "Enter Collection Name:")
    if not collection_name:
        return None, None, None  # User canceled the operation

    return folder_path, database_choice, collection_name

import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient

def parse_xml(element):
    """Recursively parse XML element and convert to JSON-like structure."""
    json_data = {}

    for child in element:
        if len(child) == 0:
            # For leaf nodes, try to convert the text value to a numeric type
            try:
                json_data[child.tag] = int(child.text)
            except ValueError:
                try:
                    json_data[child.tag] = float(child.text)
                except ValueError:
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




def upload_to_mongodb(folder_path, database_name, collection_name, mongodb_uri):
    xml_files_directory = folder_path
    import_to_mongodb(xml_files_directory, mongodb_uri, database_name, collection_name)

def upload_folder():
    folder_path, database_name, collection_name = get_user_input()
    if folder_path:
        mongodb_uri = 'mongodb://localhost:27017/'
        upload_to_mongodb(folder_path, database_name, collection_name, mongodb_uri)
        print(f"Folder uploaded to MongoDB into collection: {collection_name} in database: {database_name}")

if __name__ == "__main__":
    upload_folder()

#This script runs through the documents of a collection to identify which parameters are changing
#and which are not.The parameters that are changing go into image level report and those that are not changing
#go into run level report

import json
import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from bson import ObjectId
from pymongo import MongoClient

class MongoDBEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def traverse_document_structure(document, changes, current_path=''):
    """Traverse the document structure and identify changes in values."""
    for key, value in document.items():
        field_path = f"{current_path}.{key}" if current_path else key

        if isinstance(value, dict):
            # Recursive call for nested dictionaries
            traverse_document_structure(value, changes, field_path)
        else:
            # Check for changes in values
            if field_path not in changes:
                changes[field_path] = set()

            # Convert list to tuple for hashability
            if isinstance(value, list):
                value = tuple(value)

            changes[field_path].add(value)

def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Provide a default MongoDB URI
    #default_mongodb_uri = 'mongodb://localhost:27017/'
    mongodb_uri = 'mongodb://localhost:27017/'

    # Prompt user for MongoDB URI, database name, collection name, and destination folder
    #mongodb_uri = simpledialog.askstring("Input", f"Enter MongoDB URI (default: {default_mongodb_uri}):", initialvalue=default_mongodb_uri)
    database_name = simpledialog.askstring("Input", "Enter the database name:")
    #database_name = 'AT'
    collection_name = simpledialog.askstring("Input", "Enter the collection name:")

    folder_path = filedialog.askdirectory(title="Select Destination Folder")
    #folder_path = '/Users/mukulsherekar/pythonProject/DatabaseProject/Database_Project/Reports_AT'

    # Prompt user for filename prefixes
    constant_nodes_prefix = simpledialog.askstring("Input", "Enter the constant nodes filename suffix:")
    changed_nodes_prefix = simpledialog.askstring("Input", "Enter the changed nodes filename suffix:")

    # Automatically add "run_level" and "image_level" to the prefixes
    constant_nodes_prefix = f"run_level_{constant_nodes_prefix}" if constant_nodes_prefix else "run_level"
    changed_nodes_prefix = f"image_level_{changed_nodes_prefix}" if changed_nodes_prefix else "image_level"

    if not database_name or not collection_name or not folder_path:
        print("User input canceled.")
        return None, None, None, None, None, None

    return mongodb_uri, database_name, collection_name, folder_path, constant_nodes_prefix, changed_nodes_prefix


def export_to_json(folder_path, document, filename_prefix):
    file_path = os.path.join(folder_path, f'{filename_prefix}.json')
    with open(file_path, 'w') as json_file:
        json.dump(document, json_file, default=str, indent=2)

    print(f"Document exported to JSON file: {file_path}")

def save_json_reports(mongodb_uri, database_name, collection_name, folder_path, constant_nodes_prefix,
                      changed_nodes_prefix):
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Initialize dictionaries to track changes
    does_not_change = {}
    changes = {}

    # Traverse and identify changes in values for each document
    cursor = collection.find()
    for document in cursor:
        traverse_document_structure(document, changes)

    # Separate constant and variable values
    keys_to_remove = []
    for field_path, value_set in changes.items():
        if len(value_set) == 1:
            does_not_change[field_path] = value_set.pop()
            # Add the key to the list for removal
            keys_to_remove.append(field_path)

    # Remove keys from changes that do not change
    for key in keys_to_remove:
        del changes[key]

    # Ensure all sets are converted to lists for serialization
    does_not_change = {key: val for key, val in does_not_change.items()}
    changes = {key: list(val) for key, val in changes.items()}

    # Insert documents into MongoDB
    constant_nodes_doc = {"type": "run level data", "data": does_not_change}
    changed_nodes_doc = {"type": "image level data", "data": changes}

    # Insert documents into MongoDB
    collection.insert_one(constant_nodes_doc)
    collection.insert_one(changed_nodes_doc)

    # Print success message
    print("Documents inserted successfully.")

    # Close the MongoDB connection
    client.close()

    # Export documents to JSON files with modified filename prefixes
    export_to_json(folder_path, constant_nodes_doc, constant_nodes_prefix)
    export_to_json(folder_path, changed_nodes_doc, changed_nodes_prefix)

    # Check if the documents were inserted successfully
    print("Documents exported successfully.")

if __name__ == "__main__":
    mongodb_uri, database_name, collection_name, folder_path, constant_nodes_prefix, changed_nodes_prefix = get_user_input()

    if mongodb_uri and database_name and collection_name and folder_path and constant_nodes_prefix and changed_nodes_prefix:
        save_json_reports(mongodb_uri, database_name, collection_name, folder_path, constant_nodes_prefix,
                          changed_nodes_prefix)

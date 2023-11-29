import os
import re
import xml.etree.ElementTree as ET
from tkinter import filedialog, simpledialog
from pymongo import MongoClient
# working fine for all except date

def extract_data_from_filename(filename):
    # Extract everything except for .xml from the file name
    base_filename, _ = os.path.splitext(filename)

    # Define a regular expression pattern to match the relevant data in the filename
    pattern = r'slice_(\d+)_z=(-?\d+\.\d+)um'

    # Use re.search to find the pattern in the base filename
    match = re.search(pattern, base_filename)

    if match:
        # Extract the slice number and z-number from the matched groups
        slice_number = int(match.group(1))
        z_number = float(match.group(2))
        return base_filename, slice_number, z_number
    else:
        print("Error: Unable to extract data from the filename.")
        return None, None, None


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

def process_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return parse_xml(root)


def upload_to_mongodb(xml_files_dir, mongodb_uri, database_name, collection_name):
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    for filename in os.listdir(xml_files_dir):
        if filename.endswith(".xml"):
            # Extract slice_number and z_number from the current file
            base_filename, slice_number, z_number = extract_data_from_filename(filename)

            # Create a dictionary with filename, slice_number, and z_number
            document = {
                'filename': base_filename,
                'slice_number': slice_number,
                'z_number': z_number
            }

            # Process XML file
            json_data = process_xml_file(os.path.join(xml_files_dir, filename))

            # Add the rest of the data to the dictionary
            document.update(json_data)

            # Insert the combined dictionary into the collection
            collection.insert_one(document)



    client.close()


def upload_folder():
    folder_path, database_name, collection_name = get_user_input()
    if folder_path:
        mongodb_uri = 'mongodb://localhost:27017/'
        filename = next((f for f in os.listdir(folder_path) if f.endswith(".xml")), None)
        if filename:
            file_path = os.path.join(folder_path, filename)
            base_filename, slice_number, z_number = extract_data_from_filename(file_path)

            if base_filename is not None and  slice_number is not None and z_number is not None:
                upload_to_mongodb(folder_path, mongodb_uri, database_name, collection_name)
                print(f"Folder uploaded to MongoDB into collection: {collection_name} in database: {database_name}")
            else:
                print("Data extraction failed.")
        else:
            print("No XML files found in the folder.")

if __name__ == "__main__":
    upload_folder()

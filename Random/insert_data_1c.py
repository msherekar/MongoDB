import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient, IndexModel, ASCENDING
from tkinter import Tk, filedialog  # For UI file dialog


def parse_xml(element):
    """Recursively parse XML element and convert to JSON-like structure."""
    json_data = {}

    for child in element:
        if child.tag == "Date":
            # For the "Date" node, directly assign the text value
            json_data[child.tag] = child.text
        elif len(child) == 0:
            # For leaf nodes (excluding "Date"), directly assign the text value
            json_data[child.tag] = child.text
        else:
            # For non-leaf nodes, recursively process children
            if child.tag not in json_data:
                json_data[child.tag] = parse_xml(child)

    return json_data


def extract_unique_identifier(xml_data):
    """Extract the unique identifier (date and time) from XML data."""
    date_value = xml_data.get("Date")

    if date_value:
        # Extract only the date and time part (excluding timezone)
        return date_value.split("T")[0] + " " + date_value.split("T")[1].split(".")[0]
    else:
        # Handle missing or null "Date" field
        return None


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

            # Extract the unique identifier (date and time) from XML data
            unique_identifier = extract_unique_identifier(json_data)

            # Check if the unique identifier is present
            if unique_identifier is not None:
                # Check if a document with the same identifier exists
                existing_document = collection.find_one({"Date": unique_identifier})
                if existing_document:
                    # Warn the user about duplication
                    print(f"Warning: Duplicate document found with Date: {unique_identifier}")
                else:
                    # Insert data into MongoDB collection
                    collection.insert_one(json_data)
                    print(f"Inserted document with Date: {unique_identifier}")

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
collection_name = 'dup'

# Uncomment the next line and comment out the line after to use the UI file dialog
#xml_files_directory = get_user_input_directory()
xml_files_directory = '/Users/mukulsherekar/pythonProject/DatabaseProject/FIBSEM_Files'

# Import data into MongoDB
import_to_mongodb(xml_files_directory, mongodb_uri, database_name, collection_name)

# Connect to MongoDB for index creation
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Create a unique index on the "Date" field
index_model = IndexModel([("Date", ASCENDING)], unique=True, sparse=True)
collection.create_indexes([index_model])

# Close the MongoDB connection
client.close()

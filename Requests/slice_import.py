import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient
import re

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['demo']
collection = db['slice']

# Specify the directory containing your XML files
xml_directory = '/Users/mukulsherekar/pythonProject/DatabaseProject/FIBSEM_XMLs'

# Define the regular expression pattern to match the slice number
pattern = r'slice_(\d+)_z='

# Function to extract slice number from filename
def extract_slice_number_from_filename(filename):
    # Use re.search to find the pattern in the filename
    match = re.search(pattern, filename)

    if match:
        # Extract the matched slice number and remove leading zeros
        slice_number = int(match.group(1))
        return slice_number
    else:
        # Handle the case where the pattern is not found
        print(f"Error: Unable to extract slice number from '{filename}'.")
        return None  # or return a default value, depending on your requirements

# Iterate through XML files in the directory
for filename in os.listdir(xml_directory):
    if filename.endswith(".xml"):
        file_path = os.path.join(xml_directory, filename)

        # Extract slice number from the filename
        slice_number = extract_slice_number_from_filename(filename)

        if slice_number is not None:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Convert XML data to a dictionary (modify as per your XML structure)
            xml_data = {}
            for elem in root.iter():
                xml_data[elem.tag] = elem.text

            # Add 'slice' field to the dictionary
            xml_data['slice'] = slice_number

            # Insert the document into MongoDB
            collection.insert_one(xml_data)
        else:
            print("Document insertion skipped due to missing slice number.")

# Close the MongoDB connection
client.close()

import os
import re
import xml.etree.ElementTree as ET
from tkinter import filedialog, simpledialog
from pymongo import MongoClient
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

filename = "slice_00121_z=0.0000um.xml"
base_filename, slice_number, z_number = extract_data_from_filename(filename)

print("Base Filename:", base_filename)
print("Slice Number:", slice_number)
print("Z-Number:", z_number)

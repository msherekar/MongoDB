import re

def extract_slice_number_from_filename(filename):
    # Define the regular expression pattern to match the slice number
    pattern = r'slice_(\d+)_z='

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

import re

def extract_z_number_from_filename(filename):
    # Define a regular expression pattern to match the z-number
    pattern = r'z=(-?\d+\.\d+)um'

    # Use re.search to find the pattern in the filename
    match = re.search(pattern, filename)

    if match:
        # Extract the z-number from the matched group
        z_number = match.group(1)
        return z_number
    else:
        # Handle the case where the pattern is not found
        print("No z-number found in the filename.")
        return None  # or return a default value, depending on your requirements

# Example usage:
filename = 'slice_00121_z=0.0000um.xml'
z_number = extract_z_number_from_filename(filename)

if z_number is not None:
    print("z-number:", z_number)

# Example usage:

slice_number = extract_slice_number_from_filename(filename)

if slice_number is not None:
    print(f"Slice number for {filename}: {slice_number:5d}")
else:
    print("Slice number extraction failed.")


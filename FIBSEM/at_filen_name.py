import re

filename = "Tile_r1-c2_S_0110_663171152.xml"

# Define the regular expression pattern to extract information
pattern = r'r(\d+)-c(\d+)_S_(\d+)_(\d+)\.xml'

# Use re.search to find the pattern in the filename
match = re.search(pattern, filename)

if match:
    # Extract the information using group() method
    row_number = int(match.group(1))
    column_number = int(match.group(2))
    slice_number = int(match.group(3))
    serial_number = int(match.group(4))

    print(f"Row: {row_number}")
    print(f"Column: {column_number}")
    print(f"Slice: {slice_number}")
    print(f"Serial: {serial_number}")
else:
    print("Pattern not found in the filename.")


import re

filename = "Tile_r3-c13_S_005_1818462895.xml"

# Define the regular expression pattern to extract the name without extension
pattern = r'(.+)(\.xml)'

# Use re.search to find the pattern in the filename
match = re.search(pattern, filename)

if match:
    # Extract the name without extension using group() method
    name_without_extension = match.group(1)

    print(f"Name without extension: {name_without_extension}")
else:
    print("Pattern not found in the filename.")


from pymongo import MongoClient
from collections import Counter, defaultdict

def extract_field_values(document, field_values, current_path=''):
    """Recursively extract all unique field-value pairs from the document."""
    if isinstance(document, dict):
        for key, value in document.items():
            new_path = f"{current_path}.{key}" if current_path else key
            extract_field_values(value, field_values, new_path)
    elif isinstance(document, list):
        for i, item in enumerate(document):
            new_path = f"{current_path}.{i}" if current_path else str(i)
            extract_field_values(item, field_values, new_path)
    else:
        field_values[current_path].append(document)

def analyze_field_values(field_values):
    """Analyze the frequency of each field-value pair."""
    frequency_counter = Counter()

    for field, values in field_values.items():
        unique_values = set(values)
        frequency_counter[field] = len(unique_values)

    return frequency_counter

def identify_constant_and_varying_fields(frequency_counter):
    """Identify fields with varying values and fields with constant values."""
    constant_fields = [field for field, count in frequency_counter.items() if count == 1]
    varying_fields = [field for field, count in frequency_counter.items() if count > 1]

    return constant_fields, varying_fields

# Replace these with your actual names
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'Experimental'
collection_name = 'FIBSEM_2500'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Step 1: Extract all unique fields and their values from the documents
field_values = defaultdict(list)

for document in collection.find():
    extract_field_values(document, field_values)

# Step 2: Analyze the frequency of each field-value pair
frequency_counter = analyze_field_values(field_values)

# Step 3: Identify fields with varying values and fields with constant values
constant_fields, varying_fields = identify_constant_and_varying_fields(frequency_counter)

# Print the results
print("Constant Fields:", constant_fields)
print("Varying Fields:", varying_fields)

# Close the MongoDB connection
client.close()

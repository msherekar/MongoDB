from pymongo import MongoClient
import matplotlib.pyplot as plt
from datetime import datetime


def extract_information_for_tags(node, tags_to_extract, extracted_data):
    # Extract information from the current node
    tag = node.get('tag', '')
    text = node.get('text', '')

    # Check if the current tag is in the list of tags to extract
    if tag in tags_to_extract:
        extracted_data[tag] = text

    # Recursively extract information from child nodes
    for child_node in node.get('children', []):
        extract_information_for_tags(child_node, tags_to_extract, extracted_data)


# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'FIBSEM'

# List of tags to extract
tags_to_extract = ['Date', 'ZPos']

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Lists to store extracted data for plotting
dates = []
z_positions = []

# Traverse and extract information for specified tags from each document
for document in collection.find():
    extracted_data = {}
    extract_information_for_tags(document, tags_to_extract, extracted_data)

    # Convert the "Date" to a datetime object for better handling
    if 'Date' in extracted_data:
        extracted_data['Date'] = datetime.fromisoformat(extracted_data['Date'])

    # Append the extracted data to the lists
    dates.append(extracted_data.get('Date'))
    z_positions.append(float(extracted_data.get('ZPos', 0)))

# Close the MongoDB connection
client.close()

# Plotting
plt.plot(dates, z_positions, marker='o')
plt.xlabel('Date')
plt.ylabel('ZPos')
plt.title('ZPos over Time')
plt.show()

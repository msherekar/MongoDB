import pandas as pd
from pandas import value_counts
from pymongo import MongoClient

# Connect to your MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['demo']
collection = db['slice']

# Fetch all documents from the collection
result_cursor = collection.find()

# Initialize an empty list to store data
data = []

# Iterate through documents and extract BoundingBox values
for doc in result_cursor:
    slice = doc['slice']
    left = doc['BoundingBox.Left']
    right = doc['BoundingBox.Right']
    top = doc['BoundingBox.Top']
    bottom = doc['BoundingBox.Bottom']
    line_avg = doc['LineAvg']
    dwell = doc['Dwell']


    # Append values to the list
    data.append({
        'Slice': slice,
        'Left': left,
        'Right': right,
        'Top': top,
        'Bottom': bottom,
        'Line_Avg': line_avg,
        'Dwell': dwell

    })



# Create a DataFrame from the extracted data
df = pd.DataFrame(data)
df.to_csv('bounding_box_data.csv', index=False)

# Define a dictionary to store frequencies for each column
#frequencies_dict = {}

# Print and export unique values and frequencies for each column
for column in df.columns:
    frequencies = df[column].value_counts()

    # Print unique values and frequencies
    print(f"Unique values for {column}: {df[column].unique()}")
    print(f"Frequencies for each unique value in {column}:\n{frequencies}")




# Close the MongoDB connection
client.close()

import pandas as pd
from pandas import value_counts
from pymongo import MongoClient

# Connect to your MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['FIBSEM']
collection = db['demo']

# Fetch all documents from the collection
result_cursor = collection.find()

# Initialize an empty list to store data
data = []

# Iterate through documents and extract BoundingBox values
for doc in result_cursor:
    left = doc['Image']['BoundingBox.Left']
    right = doc['Image']['BoundingBox.Right']
    top = doc['Image']['BoundingBox.Top']
    bottom = doc['Image']['BoundingBox.Bottom']

    # Append values to the list
    data.append({
        'Left': left,
        'Right': right,
        'Top': top,
        'Bottom': bottom
    })

    # Print values for debugging
    #print(f"Left: {left}")
    #print(f"Right: {right}")
    #print(f"Top: {top}")
    #print(f"Bottom: {bottom}")

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Print the DataFrame
#print("DataFrame:")
#print(df)
# Print unique values for each column
for column in df.columns:
    unique_values = df[column].unique()
    print(f"Unique values for {column}: {unique_values}")
    print(f"Frequencies for each unique value in {column}:\n{df[column].value_counts()}")#df.to_csv('bounding_box_data.csv', index=False)

# Close the MongoDB connection
client.close()

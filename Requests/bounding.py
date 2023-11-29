import pandas as pd
from pymongo import MongoClient

# Connect to your MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['FIBSEM']
collection = db['2023_11_24']

# Fetch all documents from the collection
documents = collection.find()

# Extract BoundingBox values and store in a list
data = []
for doc in documents:
    image_info = doc.get('Image', {})
    bounding_box = image_info.get('BoundingBox', {})

    if bounding_box:
        data.append({
            'Left': bounding_box.get('Left', None),
            'Right': bounding_box.get('Right', None),
            'Top': bounding_box.get('Top', None),
            'Bottom': bounding_box.get('Bottom', None)
        })
    else:
        print(f"Skipping document with missing or empty 'BoundingBox': {doc}")

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Print information for debugging
print("Number of documents processed:", len(data))
print("DataFrame shape:", df.shape)
print("DataFrame columns:", df.columns)

# Print the DataFrame
print("DataFrame:")
print(df)

# Export the DataFrame to a CSV file
df.to_csv('bounding_box_data.csv', index=False)
print("CSV file exported successfully.")

# Close the MongoDB connection
client.close()

import pandas as pd
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
    print(doc['Image']['BoundingBox.Left'])
    #print(f"Left: {doc['Image']['BoundingBox.Left']}")
# print(f"Left: {result_list[0]['Image']['BoundingBox.Left']}")
# print(f"Right: {result_list[0]['Image']['BoundingBox.Right']}")

# print(f"Top: {result_list[0]['Image']['BoundingBox.Top']}")
# print(f"Bottom: {result_list[0]['Image']['BoundingBox.Bottom']}")

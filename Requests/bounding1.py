import pandas as pd
from pymongo import MongoClient

# Connect to your MongoDB instance
client = MongoClient('mongodb://localhost:27017/')
db = client['FIBSEM']
collection = db['demo']

# Fetch all documents from the collection
result_cursor = collection.find()

result_list = list(result_cursor)
data = []
for doc in result_list:
    left = {doc['Image']['BoundingBox.Left']}
    right = {doc['Image']['BoundingBox.Right']}
    top = {doc['Image']['BoundingBox.Top']}
    bottom = {doc['Image']['BoundingBox.Bottom']}
    print(f"Left: {doc['Image']['BoundingBox.Left']}")
    print(f"Right: {doc['Image']['BoundingBox.Right']}")
    print(f"Top: {doc['Image']['BoundingBox.Top']}")
    print(f"Bottom: {doc['Image']['BoundingBox.Bottom']}")

#print(f"Left: {result_list[0]['Image']['BoundingBox.Left']}")
#print(f"Right: {result_list[0]['Image']['BoundingBox.Right']}")

#print(f"Top: {result_list[0]['Image']['BoundingBox.Top']}")
#print(f"Bottom: {result_list[0]['Image']['BoundingBox.Bottom']}")

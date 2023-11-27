# This script has examples on how to set up query
# In this script, focus is being queried to extract
# all focus values from all doucments in a collection of a mongoDB

import pymongo

from pymongo import MongoClient

try:
    # Connect to the MongoDB server running on localhost
    client = MongoClient('localhost', 27017)

    # Access or create a database named 'test'
    db = client['Experimental']

    # Access or create a collection named 'FIBSEM'
    collection = db['FIBSEM']

    # Query Documents with a Specific Tag
    tag_to_find = "Focus"
    result = collection.find({"tag": tag_to_find})
    for document in result:
        print(document)

    # Retrieve Documents with a Specific Value in a Nested Field
    value_to_find = "Z"
    result = collection.find({"children.tag": "Application", "children.text": value_to_find})
    for document in result:
        print(document)

    # Retrieve Documents Based on a Range
    # Find documents where "Width" is greater than 9000
    result = collection.find({"children.tag": "Width", "children.text": {"$gt": "9000"}})
    for document in result:
        print(document)

    # Aggregate Data
    # Calculate the average value of "Contrast" across all documents
    result = collection.aggregate([
        {"$match": {"children.tag": "Contrast"}},
        {"$group": {"_id": None, "average_contrast": {"$avg": {"$toDouble": "$children.text"}}}}
    ])
    for document in result:
        print(document)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()

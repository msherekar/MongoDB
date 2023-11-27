import json
from pymongo import MongoClient

def extract_information_for_tags(node, tags_to_extract, extracted_info):
    tag = node.get('tag', '')
    text = node.get('text', '')

    if tag in tags_to_extract:
        extracted_info[tag] = text

    for child_node in node.get('children', []):
        extract_information_for_tags(child_node, tags_to_extract, extracted_info)

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'AT'
tags_to_extract = ['Date', 'Focus', 'Tilt units']

client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

for document in collection.find():
    print("Extracted Information:")
    extracted_info = {}
    extract_information_for_tags(document, tags_to_extract, extracted_info)

    json_filename = f"{str(document['_id'])}_extracted_info.json"
    with open(json_filename, 'w') as json_file:
        json.dump(extracted_info, json_file, indent=2)

    print(f"Saved information to {json_filename}")
    print("\n---\n")

client.close()

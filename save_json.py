import json
from bson import ObjectId
from pymongo import MongoClient

def extract_information_for_tags(node, tags_to_extract, extracted_info):
    tag = node.get('tag', '')
    text = node.get('text', '')

    if tag in tags_to_extract:
        extracted_info[tag] = text

    for child_node in node.get('children', []):
        extract_information_for_tags(child_node, tags_to_extract, extracted_info)

mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'AT'
tags_to_extract = ['Date', 'Focus', 'Tilt', 'Rot']

client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

combined_extracted_info = {}

for document in collection.find():
    print("Extracted Information:")
    extracted_info = {}
    extract_information_for_tags(document, tags_to_extract, extracted_info)

    document_id_str = str(document['_id'])
    combined_extracted_info[document_id_str] = extracted_info

    print("\n---\n")

combined_json_filename = "combined_extracted_info.json"
with open(combined_json_filename, 'w') as combined_json_file:
    json.dump(combined_extracted_info, combined_json_file, indent=2)

print(f"Saved combined information to {combined_json_filename}")

client.close()

import requests
from pymongo import MongoClient

# EMPIAR API request
empiar_api_url = "https://www.ebi.ac.uk/empiar/api/entry/11629"
response = requests.get(empiar_api_url)
if response.status_code == 200:
    empiar_data = response.json()

    # Connect to MongoDB
    mongodb_uri = 'mongodb://localhost:27017/'
    client = MongoClient(mongodb_uri)
    db = client["test"]
    collection = db["EMPIAR"]



    # Insert data into MongoDB
    result = collection.insert_one(empiar_data)
    print(f"Inserted document with ID: {result.inserted_id}")
else:
    print(f"Error: {response.status_code}, {response.text}")

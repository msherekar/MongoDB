import requests
from pymongo import MongoClient

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'emp'
empair_api_url = 'https://www.ebi.ac.uk/emdb/api/entry/10883'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Make a GET request to the EMPIAR API
response = requests.get(empair_api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Assuming the API returns JSON data
    empair_data = response.json()

    # Insert the obtained data into the MongoDB collection
    result = collection.insert_one(empair_data)

    print(f"Inserted data with ObjectId: {result.inserted_id}")
else:
    print(f"Failed to fetch data from EMPIAR API. Status code: {response.status_code}")

# Close the MongoDB connection
client.close()

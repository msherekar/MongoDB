import requests
from pymongo import MongoClient

def download_and_insert_empiar_data(empiar_id, collection_name, mongodb_uri):
    # EMPIAR API request
    empiar_api_url = f"https://www.ebi.ac.uk/empiar/api/entry/{empiar_id}"

    try:
        response = requests.get(empiar_api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        empiar_data = response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return

    # MongoDB connection
    client = MongoClient(mongodb_uri)
    db = client["AT"] # can chage this as per users requirement
    collection = db[collection_name]

    try:
        # Insert data into MongoDB
        result = collection.insert_one({"EMPIAR_Data": empiar_data})
        print(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")
    finally:
        client.close()

def get_empiar_id_and_collection():
    empiar_id = input("Enter EMPIAR ID: ")
    if not empiar_id:
        print("EMPIAR ID not provided.")
        return None, None

    collection_name = input("Enter Collection Name: ")
    if not collection_name:
        print("Collection Name not provided.")
        return None, None

    return empiar_id, collection_name

# For testing
if __name__ == "__main__":
    empiar_id, collection_name = get_empiar_id_and_collection()

    if empiar_id and collection_name:
        mongodb_uri = 'mongodb://localhost:27017/'
        download_and_insert_empiar_data(empiar_id, collection_name, mongodb_uri)

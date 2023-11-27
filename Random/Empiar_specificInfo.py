import requests
from pymongo import MongoClient


# Function to download XML data and insert into MongoDB
def download_and_insert_xml(entry_id, xml_url, db_collection):
    xml_response = requests.get(xml_url)
    if xml_response.status_code == 200:
        xml_data = xml_response.text  # You may need to parse this XML data if needed
        db_collection.update_one(
            {"entry_id": entry_id},
            {"$set": {"experimental_metadata_xml": xml_data}},
            upsert=True
        )
    else:
        print(f"Error downloading XML for entry {entry_id}: {xml_response.status_code}, {xml_response.text}")


# Make a request to the EMPIAR API
empiar_api_url = "https://www.ebi.ac.uk/empiar/api/entry/11626"
response = requests.get(empiar_api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    empiar_data = response.json()

    # Extract and process related EMDB entries
    related_emdb_entries = empiar_data.get('EMPIAR-11626', {}).get('cross_references', [])

    # Connect to MongoDB
    mongodb_uri = 'mongodb://localhost:27017/'
    client = MongoClient(mongodb_uri)
    db = client["test"]
    collection = db["EMPIAR"]

    # Insert related EMDB entries into MongoDB
    for emdb_entry in related_emdb_entries:
        collection.update_one(
            {"entry_id": emdb_entry},
            {"$set": {"related_emdb_entry": True}},
            upsert=True
        )

    # Extract and process experimental metadata
    experimental_metadata_links = empiar_data.get('EMPIAR-11629', {}).get('Experimental_metadata', [])
    print(experimental_metadata_links)

    # Iterate through metadata links and download XML data
    for metadata_link in experimental_metadata_links:
        entry_id = metadata_link.get('entry_id')
        xml_url = metadata_link.get('xml_link')
        if entry_id and xml_url:
            download_and_insert_xml(entry_id, xml_url, collection)

else:
    print(f"Error: {response.status_code}, {response.text}")

# Main EMPIAR code
# Inserts data via GUI

import tkinter as tk
from tkinter import simpledialog
import requests
from pymongo import MongoClient

def download_and_insert_empiar_data(empiar_id, collection_name):
    # EMPIAR API request
    empiar_api_url = f"https://www.ebi.ac.uk/empiar/api/entry/{empiar_id}"
    response = requests.get(empiar_api_url)

    # MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client["test"]
    collection = db[collection_name]

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        empiar_data = response.json()
        print(empiar_data)

        # Insert data into MongoDB
        result = collection.insert_one({"EMPIAR_Data": empiar_data})
        print(f"Inserted document with ID: {result.inserted_id}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_empiar_id_and_collection():
    empiar_id = simpledialog.askstring("EMPIAR ID", "Enter EMPIAR ID:")
    collection_name = simpledialog.askstring("Collection Name", "Enter Collection Name:")
    return empiar_id, collection_name

def main():
    # Create Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get EMPIAR ID and Collection Name from user
    empiar_id, collection_name = get_empiar_id_and_collection()

    if empiar_id and collection_name:
        # Download and insert EMPIAR data
        download_and_insert_empiar_data(empiar_id, collection_name)

if __name__ == "__main__":
    main()

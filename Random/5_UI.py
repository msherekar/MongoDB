import tkinter as tk
from tkinter import filedialog, simpledialog
import requests
from pymongo import MongoClient
import os
import xml.etree.ElementTree as ET

class MongoDBGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MongoDB GUI")

        # Buttons
        self.upload_button = tk.Button(master, text="Upload", command=self.upload_folder)
        self.upload_button.grid(row=0, column=1, padx=10, pady=10)

        self.plot_button = tk.Button(master, text="Plots", command=self.run_plot_script)
        self.plot_button.grid(row=1, column=0, padx=10, pady=10)

        self.query_button = tk.Button(master, text="Queries", command=self.show_query_buttons)
        self.query_button.grid(row=1, column=1, padx=10, pady=10)

        self.reports_button = tk.Button(master, text="Reports", command=self.run_report_script)
        self.reports_button.grid(row=1, column=2, padx=10, pady=10)

        # EMPIAR button
        self.empiar_button = tk.Button(master, text="EMPIAR", command=self.run_empiar_script)
        self.empiar_button.grid(row=2, column=1, padx=10, pady=10)

        # Query buttons (initially hidden)
        self.query_buttons = []
        for i in range(1, 4):
            query_button = tk.Button(master, text=f"Query {i}", command=lambda i=i: self.run_query_script(i))
            self.query_buttons.append(query_button)
            query_button.grid(row=2, column=i, padx=10, pady=10)
            query_button.grid_remove()

    def upload_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            # Prompt user for collection name
            collection_name = simpledialog.askstring("Collection Name", "Enter Collection Name:")
            if collection_name:
                self.upload_to_mongodb(folder_path, collection_name)
                print(f"Folder uploaded to MongoDB into collection: {collection_name}")

    def upload_to_mongodb(self, folder_path, collection_name):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['AT']
        collection = db[collection_name]

        # Iterate through XML files in the directory
        for filename in os.listdir(folder_path):
            if filename.endswith(".xml"):
                file_path = os.path.join(folder_path, filename)

                # Parse XML
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Convert XML to JSON-like structure
                json_data = self.parse_xml(root)

                # Insert data into MongoDB collection
                collection.insert_one(json_data)

        # Close the MongoDB connection
        client.close()

    def parse_xml(self, element):
        """Recursively parse XML element and convert to JSON-like structure."""
        json_data = {}

        for child in element:
            if len(child) == 0:
                # For leaf nodes, directly assign the text value
                json_data[child.tag] = child.text
            else:
                # For non-leaf nodes, recursively process children
                if child.tag not in json_data:
                    json_data[child.tag] = self.parse_xml(child)

        return json_data

    def show_query_buttons(self):
        # Show query buttons
        for query_button in self.query_buttons:
            query_button.grid()

    def run_plot_script(self):
        # Implement script to generate various plots
        print("Running plot script...")

    def run_report_script(self):
        # Implement script to generate reports
        print("Running report script...")

    def run_query_script(self, query_number):
        # Implement script for each query button
        print(f"Running query script {query_number}...")

    def run_empiar_script(self):
        # Get EMPIAR ID and Collection Name from user
        empiar_id, collection_name = self.get_empiar_id_and_collection()

        if empiar_id and collection_name:
            # Download and insert EMPIAR data
            self.download_and_insert_empiar_data(empiar_id, collection_name)

    def download_and_insert_empiar_data(self, empiar_id, collection_name):
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

    def get_empiar_id_and_collection(self):
        empiar_id = simpledialog.askstring("EMPIAR ID", "Enter EMPIAR ID:")
        collection_name = simpledialog.askstring("Collection Name", "Enter Collection Name:")
        return empiar_id, collection_name

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBGUI(root)
    root.mainloop()

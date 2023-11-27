import tkinter as tk
from pymongo import MongoClient
import matplotlib.pyplot as plt

class MongoDBUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MongoDB UI")

        # Buttons
        self.query_button = tk.Button(master, text="Query", command=self.run_query)
        self.query_button.grid(row=0, column=0, padx=10, pady=10)

        self.plot_button = tk.Button(master, text="Plots", command=self.plot_data)
        self.plot_button.grid(row=0, column=1, padx=10, pady=10)

    def run_query(self):
        # Replace the print statement with the logic from your provided code

        # Replace these with your actual values
        mongodb_uri = 'mongodb://localhost:27017/'
        database_name = 'Experimental'
        collection_name = 'FIBSEM'

        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Traverse and extract information from each document
        for document in collection.find():
            print("Extracted Information:")
            self.extract_information(document)
            print("\n---\n")

        # Close the MongoDB connection
        client.close()

    def extract_information(self, node):
        # Extract information from the current node
        tag = node.get('tag', '')
        text = node.get('text', '')

        # If the tag is "Focus", print its text
        if tag == 'Focus':
            print(f"Focus: {text}")

        # Recursively extract information from child nodes
        for child_node in node.get('children', []):
            self.extract_information(child_node)

    def plot_data(self):
        print("Plotting Data...")

        # Replace these with your actual values
        mongodb_uri = 'mongodb://localhost:27017/'
        database_name = 'Experimental'
        collection_name = 'FIBSEM'

        # List of tags to extract
        tags_to_extract = ['ZPos', 'Z']

        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Extracted data
        extracted_data = {tag: [] for tag in tags_to_extract}

        # Traverse and extract information for specified tags from each document
        for document in collection.find():
            self.extract_information_for_tags(document, tags_to_extract, extracted_data)

        # Close the MongoDB connection
        client.close()

        # Plot scatter plots for ZPos and Z values
        plt.scatter(extracted_data['ZPos'], extracted_data['ZPos'], label='Scatter Plot ZPos')
        plt.xlabel('Document Index')
        plt.ylabel('ZPos')
        plt.title('Scatter Plot of ZPos')
        plt.legend()
        plt.show()

        plt.scatter(extracted_data['Z'], extracted_data['Z'], label='Scatter Plot Z')
        plt.xlabel('Document Index')
        plt.ylabel('Z')
        plt.title('Scatter Plot of Z')
        plt.legend()
        plt.show()

    def extract_information_for_tags(self, node, tags_to_extract, extracted_data):
        # Extract information from the current node
        tag = node.get('tag', '')
        text = node.get('text', '')

        # Check if the current tag is in the list of tags to extract
        if tag in tags_to_extract:
            extracted_data[tag].append(float(text))

        # Recursively extract information from child nodes
        for child_node in node.get('children', []):
            self.extract_information_for_tags(child_node, tags_to_extract, extracted_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBUI(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from PIL import Image, ImageTk

class MongoDBGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MongoDB GUI")

        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['test']  # Replace 'your_database' with your actual database name
        self.collection = self.db['AT']  # Replace 'your_collection' with your actual collection name

        # GUI components
        self.label = tk.Label(master, text="Enter Document:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.insert_button = tk.Button(master, text="Insert Document", command=self.insert_document)
        self.insert_button.pack()

        self.query_button = tk.Button(master, text="Query Documents", command=self.display_document_window)
        self.query_button.pack()

    def insert_document(self):
        document_text = self.entry.get()
        document = {"data": document_text}
        self.collection.insert_one(document)
        print("Document inserted:", document)

    def display_document_window(self):
        # Create a new Toplevel window
        document_window = tk.Toplevel(self.master)
        document_window.title("Document View")

        # Get the structure of the documents
        structure = self.get_document_structure()

        # Create a box for each node, sub-node, and child node
        for node, sub_nodes in structure.items():
            node_frame = ttk.Frame(document_window)
            node_frame.pack(side=tk.LEFT, padx=10, pady=10)

            # Create a label for the node
            node_label = tk.Label(node_frame, text=node, font=("Helvetica", 10, "bold"))
            node_label.pack()

            # Create labels with icons for sub-nodes and child nodes
            for sub_node in sub_nodes:
                self.create_icon_label(node_frame, sub_node)

    def create_icon_label(self, parent_frame, sub_node):
        # Load and resize the icon (replace 'icon.png' with the actual file name)
        icon_path = 'icon.png'
        icon = Image.open(icon_path)
        icon = icon.resize((30, 30), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(icon)

        # Create a label with the icon
        icon_label = tk.Label(parent_frame, image=icon, text=sub_node, compound=tk.LEFT)
        icon_label.image = icon
        icon_label.pack()

    def get_document_structure(self):
        # Retrieve a sample document to determine its structure
        sample_document = self.collection.find_one()

        # Traverse the document structure and extract nodes, sub-nodes, and child nodes
        structure = {}
        self.extract_structure("", sample_document, structure)
        return structure

    def extract_structure(self, parent, document, structure):
        for key, value in document.items():
            node = key if parent == "" else f"{parent}.{key}"
            structure[node] = []

            if isinstance(value, dict):
                sub_nodes = self.extract_structure(node, value, structure)
                structure[node].extend(sub_nodes)
            else:
                structure[parent].append(value)

        # Return an empty list if parent is not in the structure dictionary
        return structure.get(parent, [])

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBGUI(root)
    root.mainloop()

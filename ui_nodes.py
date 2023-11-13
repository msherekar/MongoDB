import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient

class MongoDBGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MongoDB GUI")

        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['your_database']  # Replace 'your_database' with your actual database name
        self.collection = self.db['your_collection']  # Replace 'your_collection' with your actual collection name

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

        # Treeview for displaying documents
        tree = ttk.Treeview(document_window)
        tree["columns"] = ("Field", "Value")
        tree.column("#0", width=150, minwidth=150)
        tree.column("Field", anchor=tk.W, width=150)
        tree.column("Value", anchor=tk.W, width=150)
        tree.heading("#0", text="Document")
        tree.heading("Field", text="Field")
        tree.heading("Value", text="Value")

        # Query and display documents in the Treeview
        self.query_documents(tree)

        tree.pack()

    def query_documents(self, tree):
        # Clear previous entries in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        documents = self.collection.find()
        for idx, doc in enumerate(documents, start=1):
            parent_node = tree.insert("", "end", text=f"Document {idx}")
            self.display_document_structure(tree, parent_node, doc, "")

    def display_document_structure(self, tree, parent, document, parent_key):
        for key, value in document.items():
            item = tree.insert(parent, "end", text=key if parent_key == "" else f"{parent_key}.{key}")
            if isinstance(value, dict):
                self.display_document_structure(tree, item, value, key)
            else:
                tree.insert(item, "end", values=("", str(value)))

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBGUI(root)
    root.mainloop()

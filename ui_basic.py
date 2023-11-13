import tkinter as tk
from pymongo import MongoClient

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

        self.query_button = tk.Button(master, text="Query Documents", command=self.query_documents)
        self.query_button.pack()

    def insert_document(self):
        document_text = self.entry.get()
        document = {"data": document_text}
        self.collection.insert_one(document)
        print("Document inserted:", document)

    def query_documents(self):
        documents = self.collection.find()
        print("All Documents:")
        for doc in documents:
            print(doc)

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBGUI(root)
    root.mainloop()

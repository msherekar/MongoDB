import tkinter as tk
from tkinter import ttk

from pymongo import MongoClient

class MongoDBUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MongoDB Desktop App")

        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['test']  # Replace 'your_database' with your actual database name
        self.collection = self.db['FIBSEM']  # Replace 'your_collection' with your actual collection name

        # UI components
        self.label = tk.Label(master, text="MongoDB Desktop App", font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Button to fetch data
        self.fetch_button = tk.Button(master, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.grid(row=1, column=0, pady=10)

        # Treeview to display data
        self.tree = ttk.Treeview(master, columns=('Column 1', 'Column 2'))  # Adjust columns as needed
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def fetch_data(self):
        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve data from MongoDB and populate Treeview
        data = self.collection.find()  # Replace with your query
        for item in data:
            self.tree.insert('', 'end', values=(item['Field1'], item['Field2']))  # Adjust fields as needed

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBUI(root)
    root.mainloop()

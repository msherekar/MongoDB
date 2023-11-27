import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient

class MongoDBQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MongoDB Query App")

        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['test']
        self.collection = self.db['FIBSEM']

        # Create and layout widgets
        self.create_widgets()

    def create_widgets(self):
        # Application section
        self.create_label_and_entry("Application Version:", "Application.Version")
        self.create_label_and_entry("Application Date:", "Application.Date")

        # Image section
        self.create_label_and_entry("Image Width:", "Image.Width")
        self.create_label_and_entry("Image Height:", "Image.Height")
        self.create_label_and_entry("Image Machine:", "Image.Machine")

        # Scan section
        self.create_label_and_entry("Scan Dwell:", "Scan.Dwell")
        self.create_label_and_entry("Scan FOV_X:", "Scan.FOV_X")

        # Stage section
        self.create_label_and_entry("Stage X:", "Stage.X")
        self.create_label_and_entry("Stage Y:", "Stage.Y")

        # ATLAS3D section
        self.create_label_and_entry("ATLAS3D Stack ID:", "ATLAS3D.Stack.ID")
        self.create_label_and_entry("ATLAS3D Stack Name:", "ATLAS3D.Stack.Name")
        self.create_label_and_entry("ATLAS3D Slice ZPos:", "ATLAS3D.Stack.Slice.ZPos")

        # Query button
        self.query_button = ttk.Button(self.root, text="Submit Query", command=self.submit_query)
        self.query_button.grid(row=15, column=0, columnspan=2, pady=10)

        # Display area for results
        self.results_text = tk.Text(self.root, height=10, width=40, wrap=tk.WORD)
        self.results_text.grid(row=16, column=0, columnspan=2, padx=10, pady=5)

    def create_label_and_entry(self, label_text, node_path):
        label = ttk.Label(self.root, text=label_text)
        label.grid(sticky=tk.W, row=self.root.grid_size()[1], column=0, padx=10, pady=5)

        entry = ttk.Entry(self.root)
        entry.grid(row=self.root.grid_size()[1] - 1, column=1, padx=10, pady=5)

        setattr(self, f"{node_path.replace('.', '_')}_entry", entry)

    def submit_query(self):
        try:
            # Build query based on user-entered values
            query = {}
            for child in self.root.winfo_children():
                if isinstance(child, ttk.Entry):
                    node_path = child.get()
                    value = child.get()
                    if value:
                        query[node_path] = value

            # Query documents based on user-input
            cursor = self.collection.find(query)

            # Display results in the text widget
            result_text = ""
            for document in cursor:
                result_text += f"Document ID: {document['_id']['$oid']}\n"
                for key, value in document.items():
                    result_text += f"{key}: {value}\n"
                result_text += "\n"

            self.results_text.delete(1.0, tk.END)  # Clear previous results
            self.results_text.insert(tk.END, result_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBQueryApp(root)
    app.run()

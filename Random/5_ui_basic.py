import tkinter as tk
from tkinter import filedialog
from pymongo import MongoClient

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
            self.upload_to_mongodb(folder_path)
            print("Folder uploaded to MongoDB.")

    def upload_to_mongodb(self, folder_path):
        # Implement MongoDB upload logic here
        pass

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

    def run_empiar_script(self,):
        print("Running empiar script...")

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBGUI(root)
    root.mainloop()

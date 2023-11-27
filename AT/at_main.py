import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, simpledialog
from pymongo import MongoClient
from at_upload import upload_folder
from at_plot import generate_scatter_plots, get_user_input, run_plot_script
from at_query import RowCol,mosaic,tileposition
import at_empiar
from at_report import save_json_reports, get_user_input
class MongoDBGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MongoDB GUI")

        # Buttons
        self.upload_button = tk.Button(master, text="Upload", command=self.upload_folder)
        self.upload_button.grid(row=0, column=1, padx=10, pady=10)

        self.plot_button = tk.Button(master, text="Plots", command=self.run_plot_script)
        self.plot_button.grid(row=1, column=0, padx=10, pady=10)

        # Buttons
        self.query_button = tk.Button(master, text="Queries", command=self.show_query_buttons)
        self.query_button.grid(row=1, column=1, padx=10, pady=10)

        self.reports_button = tk.Button(master, text="Reports", command=self.export_files)
        self.reports_button.grid(row=1, column=2, padx=10, pady=10)

        self.empiar_button = tk.Button(master, text="EMPIAR", command=self.run_empiar_script)
        self.empiar_button.grid(row=3, column=1, padx=10, pady=10)

        # Query buttons (initially hidden)
        self.query_buttons = []
        for i in range(1, 3):
            query_button = tk.Button(master, text=f"Query {i}", command=lambda i=i: self.show_query_buttons(i))
            self.query_buttons.append(query_button)
            query_button.grid(row=2, column=i, padx=10, pady=10)
            query_button.grid_remove()

    def upload_folder(self):
        upload_folder()
        print("Uploaded folder to MongoDB.")

    def export_files(self):
        # Get user input for MongoDB URI and other parameters
        mongodb_uri, database_name, collection_name, folder_path, constant_nodes_prefix, changed_nodes_prefix = get_user_input()

        # Call the save_json_reports function with the obtained parameters
        if mongodb_uri and database_name and collection_name and folder_path and constant_nodes_prefix and changed_nodes_prefix:
            save_json_reports(mongodb_uri, database_name, collection_name, folder_path,
                              constant_nodes_prefix, changed_nodes_prefix)

    def show_query_buttons(self):
        # Create a Toplevel dialog for Query-1
        query1_dialog = tk.Toplevel(self.master)
        query1_button = tk.Button(query1_dialog, text="Search by Row & Column",
                                  command=lambda: self.run_query_dialog(query1_dialog, RowCol))
        query1_button.pack(pady=10)

        # Create a Toplevel dialog for Query-2
        query2_dialog = tk.Toplevel(self.master)
        query2_button = tk.Button(query2_dialog, text="Search for Mosaic Information",
                                  command=lambda: self.run_query_dialog(query2_dialog, mosaic))
        query2_button.pack(pady=10)

        # Create a Toplevel dialog for Query-3
        query3_dialog = tk.Toplevel(self.master)
        query3_button = tk.Button(query3_dialog, text="Search for Tile Position History",
                                  command=lambda: self.run_query_dialog(query3_dialog, tileposition))
        query3_button.pack(pady=10)

    def run_query_dialog(self, dialog, query_function):
        try:
            # Get user input for collection name
            collection_name = self.collection()

            # Ask user for $gte and $lte values using dialog boxes
            row = simpledialog.askinteger("Input", "Enter row:")
            column = simpledialog.askinteger("Input", "Enter column:")

            print(f"Received values: Row Number ={row}, Column Number={column}")

            # Call the specified query function with user-provided values
            result = query_function(collection_name, row, column)

            print("Query executed, result:")
            for document in result:
                print(document)

            # You can display the result in a widget or perform any other desired action here

        except Exception as e:
            print(f"An error occurred in run_query_dialog: {e}")

    def collection(self):
        # Ask user for collection names using dialog boxes
        collection_name = simpledialog.askstring("Input", "Enter collection name:")
        return collection_name

    def run_plot_script(self):
        run_plot_script()


    def run_empiar_script(self):
        # Prompt user for EMPIAR ID and Collection Name
        empiar_id = simpledialog.askstring("EMPIAR ID", "Enter EMPIAR ID:")
        if not empiar_id:
            print("EMPIAR ID input canceled.")
            return

        collection_name = simpledialog.askstring("Collection Name", "Enter Collection Name:")
        if not collection_name:
            print("Collection Name input canceled.")
            return
        mongodb_uri = 'mongodb://localhost:27017/'
        # Now you have the EMPIAR ID and Collection Name, proceed with the script
        at_empiar.download_and_insert_empiar_data(empiar_id, collection_name,mongodb_uri)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")

    app = MongoDBGUI(root)

    root.mainloop()

#Users/mukulsherekar/pythonProject/DatabaseProject
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, simpledialog,Button,Text
from pymongo import MongoClient
from Module_upload1 import upload_folder
from Module_plot1 import generate_scatter_plots, get_user_input, run_plot_script
from Module_query1 import run_query_by_slice_number,get_database_and_collection
import Module_empiar
from Module_report import save_json_reports, get_user_input
class MongoDBGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MongoDB GUI")

        # Buttons
        self.upload_button = tk.Button(master, text="Upload", command=self.upload_folder)
        self.upload_button.grid(row=0, column=1, padx=10, pady=10)

        # Buttons
        self.query_button = Button(master, text="Query", command=self.run_query_dialog)
        self.query_button.grid(row=1, column=1, padx=10, pady=10)

    

        self.reports_button = tk.Button(master, text="Reports", command=self.export_files)
        self.reports_button.grid(row=1, column=2, padx=10, pady=10)

        self.empiar_button = tk.Button(master, text="EMPIAR", command=self.run_empiar_script)
        self.empiar_button.grid(row=2, column=1, padx=10, pady=10)


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

    def run_query_dialog(self):
        try:
            # Get user input for database and collection names
            database_name, collection_name = get_database_and_collection()

            print(f"Database: {database_name}, Collection: {collection_name}")

            # Ask user for $gte and $lte values using dialog boxes
            gte_value = simpledialog.askinteger("Input", "Enter $gte value:")
            lte_value = simpledialog.askinteger("Input", "Enter $lte value:")

            print(f"Received values: gte={gte_value}, lte={lte_value}")

            # Call the Query-1 module with user-provided values
            result = run_query_by_slice_number(database_name, collection_name, gte_value, lte_value)

            print("Query executed, result:")
            for document in result:
                print(document)



        except Exception as e:
            print(f"An error occurred in run_query_dialog: {e}")



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
        Module_empiar.download_and_insert_empiar_data(empiar_id, collection_name,mongodb_uri)




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Application")

    app = MongoDBGUI(root)

    print("Before main loop")
    root.mainloop()
    print("After main loop")
#Users/mukulsherekar/pythonProject/DatabaseProject
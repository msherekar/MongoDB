# plot_module.py
import os
import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from pymongo import MongoClient

def get_user_input():
    # Get database name
    #database_name = simpledialog.askstring("Database Name", "Enter Database Name:")
    database_name = 'FIBSEM'
    if not database_name:
        return None, None, None, None  # User canceled the operation

    # Get collection name
    collection_name = simpledialog.askstring("Collection Name", "Enter Collection Name:")
    if not collection_name:
        return None, None, None, None  # User canceled the operation

    # Get folder to save plots
    #folder_path = simpledialog.askstring("Folder Path", "Enter Folder Path to Save Plots:")
    folder_path = '/Users/mukulsherekar/pythonProject/DatabaseProject/Database_Project/Reports_FIBSEM'
    if not folder_path:
        return None, None, None, None  # User canceled the operation

    # Get parameter name
    #parameter_name = simpledialog.askstring("Parameter Name", "Enter Parameter Name:")
    parameter_name = 'ZPos'
    if not parameter_name:
        return None, None, None, None  # User canceled the operation

    return database_name, collection_name, folder_path, parameter_name

def plot_parameter(data, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for key, values in data.items():
        if key not in ['_id', 'Application.Date', 'type']:
            plt.figure()
            plt.scatter(range(1, len(values) + 1), values, s=5)
            plt.xlabel('Data Point')
            plt.ylabel(f'{key} Values')
            plt.title(f'Scatter Plot for {key}')
            plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

            plot_file_path = os.path.join(folder_path, f'{key}_scatter_plot.png')
            plt.savefig(plot_file_path)

            plt.close()
            print(f"Scatter plot for {key} saved at: {plot_file_path}")

def generate_scatter_plots(database_name, collection_name, folder_path, parameter_name):
    mongodb_uri = 'mongodb://localhost:27017/'

    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    document = collection.find_one({'type': 'image level data'})

    if not document:
        print(f"No document found in collection: {collection_name} with 'type': 'image level data'")
        return

    data = document.get('data', {})
    plot_parameter(data, folder_path)

    print(f"Scatter plots generated for all keys in document with 'type': 'image level data' in collection: {collection_name}.")

def run_plot_script():
    database_name, collection_name, folder_path, parameter_name = get_user_input()
    if database_name is not None:
        generate_scatter_plots(database_name, collection_name, folder_path, parameter_name)

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from pymongo import MongoClient

# Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['FIBSEM']
collection = db['Experimental']

# Define the Entry widgets globally
entry_fixed_number = None
entry_min_range = None
entry_max_range = None

def query_by_fixed_number():
    global entry_fixed_number
    target_zindex = simpledialog.askstring("Input", "Enter ZIndex for Query by Fixed Number:")
    if target_zindex is not None:
        query = {"ATLAS3D.Slice.ZIndex": target_zindex}
        execute_query(query)

def query_by_range():
    global entry_min_range, entry_max_range
    min_zindex = simpledialog.askstring("Input", "Enter Min ZIndex for Query by Range:")
    max_zindex = simpledialog.askstring("Input", "Enter Max ZIndex for Query by Range:")
    if min_zindex is not None and max_zindex is not None:
        query = {"ATLAS3D.Slice.ZIndex": {"$gte": min_zindex, "$lte": max_zindex}}
        execute_query(query)

def execute_query(query):
    result = collection.find(query)
    # Process and display the results as needed
    for document in result:
        print(document)

# Main window
root = tk.Tk()
root.title("MongoDB Query UI")

def open_query_window():
    global entry_fixed_number, entry_min_range, entry_max_range

    query_window = tk.Toplevel(root)
    query_window.title("Query Options")

    # Button for Query by Fixed Number
    btn_fixed_number = ttk.Button(query_window, text="Query by Fixed Number", command=query_by_fixed_number)
    btn_fixed_number.pack()

    # Button for Query by Range
    btn_range = ttk.Button(query_window, text="Query by Range", command=query_by_range)
    btn_range.pack()

# Button for opening Query Options window
btn_query = ttk.Button(root, text="Query", command=open_query_window)
btn_query.pack()

# Run the main loop
root.mainloop()

from pymongo import MongoClient
import tkinter as tk
from tkinter import Label, Entry, Button


def run_match_query(db_name, collection_name, gte_value, lte_value):
    # Connect to the MongoDB server running on localhost at port 27017
    client = MongoClient('mongodb://localhost:27017/')

    # Perform a $match query on the specified collection of the specified database
    result = client[db_name][collection_name].aggregate([
        {
            '$match': {
                'ATLAS3D.Slice.ZIndex': {
                    '$gte': gte_value,
                    '$lte': lte_value
                }
            }
        }
    ])

    # Print the matching documents
    for document in result:
        print(document)


def run_aggregate_query(db_name, collection_name):
    # Connect to the MongoDB server running on localhost at port 27017
    client = MongoClient('mongodb://localhost:27017/')

    # Perform an aggregation query on the specified collection of the specified database
    result = client[db_name][collection_name].aggregate([
        # Add your aggregation stages here
        # Example: {'$group': {'_id': '$someField', 'count': {'$sum': 1}}}
    ])

    # Print the aggregated result
    for document in result:
        print(document)


def on_match_submit():
    # Retrieve values from the Entry widgets
    db_name = db_entry.get()
    collection_name = collection_entry.get()
    gte_value = int(gte_entry.get())
    lte_value = int(lte_entry.get())

    # Run the $match MongoDB query with the user-provided values
    run_match_query(db_name, collection_name, gte_value, lte_value)


def on_aggregate_submit():
    # Retrieve values from the Entry widgets
    db_name = db_entry.get()
    collection_name = collection_entry.get()

    # Run the $aggregate MongoDB query with the user-provided values
    run_aggregate_query(db_name, collection_name)


# Create the main window
root = tk.Tk()
root.title("MongoDB Query UI")

# Create and place Label and Entry widgets for database name
Label(root, text="Database Name:").grid(row=0, column=0, padx=10, pady=10)
db_entry = Entry(root)
db_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place Label and Entry widgets for collection name
Label(root, text="Collection Name:").grid(row=1, column=0, padx=10, pady=10)
collection_entry = Entry(root)
collection_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place Label and Entry widgets for $gte
Label(root, text="$gte:").grid(row=2, column=0, padx=10, pady=10)
gte_entry = Entry(root)
gte_entry.grid(row=2, column=1, padx=10, pady=10)

# Create and place Label and Entry widgets for $lte
Label(root, text="$lte:").grid(row=3, column=0, padx=10, pady=10)
lte_entry = Entry(root)
lte_entry.grid(row=3, column=1, padx=10, pady=10)

# Create and place the $match Submit Button
match_submit_button = Button(root, text="$match Submit", command=on_match_submit)
match_submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create and place the $aggregate Submit Button
aggregate_submit_button = Button(root, text="$aggregate Submit", command=on_aggregate_submit)
aggregate_submit_button.grid(row=5, column=0, columnspan=2, pady=10)

# Start the Tkinter main loop
root.mainloop()

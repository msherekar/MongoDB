import matplotlib.pyplot as plt
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'FIBSEM'
collection_name = 'Experimental'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Find documents with "Type": "changed_nodes"
documents = collection.find({'type': 'changed_nodes'})

# Iterate over selected documents
for document in documents:
    # Access the "data" key
    data = document.get('data', {})

    # Extract node names and values
    node_names = [node_name for node_name in data.keys() if node_name not in ['_id', 'Application.Date']]
    node_values = [data[node_name] for node_name in node_names]

    # Plot scatter plots for each node under "data"
    for i, (node_name, node_data) in enumerate(zip(node_names, node_values)):
        plt.figure()  # Create a new figure for each node
        plt.scatter(range(1, len(node_data) + 1), node_data, s=5)  # Use range for x-axis
        plt.xlabel('Data Point')
        plt.ylabel('Node Values')
        plt.title(f'Scatter Plot for Node: {node_name}')
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        #plt.savefig(f'{node_name}_scatter_plot.png')  # Save each plot as an image file
        plt.show()
        plt.close()  # Close the current figure to start a new one for the next node

print("Scatter plots generated for each node in documents with 'Type': 'changed_nodes'.")

# Close the MongoDB connection
client.close()


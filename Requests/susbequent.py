from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
collection = client['FIBSEM']['test9']

# Define the aggregation pipeline
pipeline = [
    {
        '$project': {
            'ATLAS3D.Slice.ZPos': 1,
            'ATLAS3D.Slice.NominalZPos': 1,
            'slice_number': 1
        }
    },
    {
        '$sort': {
            'slice_number': 1
        }
    },
    {
        '$limit': 100  # Limit to the first 100 slices
    }
]

# Run the aggregation pipeline
result = list(collection.aggregate(pipeline))

# Extract values for plotting
slice_numbers = [doc['slice_number'] for doc in result]
z_pos_values = [round(doc['ATLAS3D']['Slice']['ZPos'], 4) for doc in result]
nominal_z_pos_values = [round(doc['ATLAS3D']['Slice']['NominalZPos'], 4) for doc in result]

# Calculate subsequent differences
z_pos_diff = np.diff(z_pos_values)
nominal_z_pos_diff = np.diff(nominal_z_pos_values)
print(z_pos_diff)
# Plot the values as scatter plots
plt.scatter(slice_numbers[:-1], z_pos_diff, label='ZPos Differences', marker='o')
plt.scatter(slice_numbers[:-1], nominal_z_pos_diff, label='NominalZPos Differences', marker='x')

# Customize the plot
plt.xlabel('Slice Numbers')
plt.ylabel('Differences')
plt.title('Subsequent Differences: ZPos and NominalZPos (First 100 Slices)')
plt.legend()
plt.show()

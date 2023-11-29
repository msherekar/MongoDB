from pymongo import MongoClient
import matplotlib.pyplot as plt

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
    }
]

# Run the aggregation pipeline
result = list(collection.aggregate(pipeline))

# Extract values for plotting
slice_numbers = [doc['slice_number'] for doc in result]
z_pos_values = [round(doc['ATLAS3D']['Slice']['ZPos'], 4) for doc in result]
nominal_z_pos_values = [round(doc['ATLAS3D']['Slice']['NominalZPos'], 4) for doc in result]
#print(z_pos_values)
# Plot the values
plt.scatter(slice_numbers, z_pos_values, label='ZPos', marker='o')
plt.scatter(slice_numbers, nominal_z_pos_values, label='Nominal ZPos', marker='x')

# Customize the plot
plt.xlabel('Slice Numbers')
plt.ylabel('Values (um)')
plt.title('ZPos and Nominal ZPos')
plt.legend()
plt.show()

# Example: Print ZPos and NominalZPos for a specific slice number (e.g., slice_number = 5)
target_slice_number = 2500
index_of_slice = slice_numbers.index(target_slice_number)

if index_of_slice != -1:
    print(f"ZPos for slice {target_slice_number}: {z_pos_values[index_of_slice]}")
    print(f"NominalZPos for slice {target_slice_number}: {nominal_z_pos_values[index_of_slice]}")
else:
    print(f"Slice number {target_slice_number} not found.")
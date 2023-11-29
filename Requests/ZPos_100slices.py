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

# Plot the values as scatter plots
plt.plot(slice_numbers, z_pos_values, label='ZPos')
plt.plot(slice_numbers, nominal_z_pos_values, label='Nominal ZPos')

# Customize the plot
plt.xlabel('Slice Numbers')
plt.ylabel('Values')
plt.title('Scatter Plot: ZPos and Nominal ZPos (First 100 Slices)')
plt.legend()
plt.show()

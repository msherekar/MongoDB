from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['FIBSEM']
collection = db['test9']

# Aggregate to calculate average values
result = collection.aggregate([
    {
        '$group': {
            '_id': None,
            'avgStageX': {'$avg': '$Stage.X'},
            'avgStageY': {'$avg': '$Stage.Y'},
            'avgSystemVacuum': {'$avg': '$Microscope.SystemVacuum'}
        }
    }
])

# Extract the result
avg_values = list(result)[0] if result.alive else None

# Format and print the average values with scientific notation
if avg_values:
    avg_stage_x = avg_values['avgStageX']
    avg_stage_y = avg_values['avgStageY']
    avg_system_vacuum = avg_values['avgSystemVacuum']

    print(f"Avg StageX: {avg_stage_x:.4e} um")
    print(f"Avg StageY: {avg_stage_y:.4e} um")
    print(f"Avg SystemVacuum: {avg_system_vacuum:.4e} mbar")
else:
    print("No data available.")

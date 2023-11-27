from pymongo import MongoClient

# Replace these with your actual values
mongodb_uri = 'mongodb://localhost:27017/'
database_name = 'test'
collection_name = 'AT'

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]

# Count the number of documents
num_documents = collection.count_documents({})

print(f"Number of Documents: {num_documents}")

# Traverse and print the type of each document
cursor = collection.find()
for document in cursor:
    document_type = type(document)
    print(f"Document Type: {document_type}")
    # You can print or process other information about the document here

# Close the MongoDB connection
client.close()

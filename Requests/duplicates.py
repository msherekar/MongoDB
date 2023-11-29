from pymongo import MongoClient

def upload_to_mongodb(xml_files_dir, mongodb_uri, database_name, collection_name):
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    for filename in os.listdir(xml_files_dir):
        if filename.endswith(".xml"):
            file_path = os.path.join(xml_files_dir, filename)

            # Extract slice_number and z_number from the current file
            base_filename, slice_number, z_number = extract_data_from_filename(file_path)

            # Process XML file
            json_data = process_xml_file(file_path)

            # If slice_number and z_number are available, add them to the JSON data
            if base_filename is not None and slice_number is not None and z_number is not None:
                json_data['filename'] = base_filename
                json_data['slice_number'] = slice_number
                json_data['z_number'] = z_number

                # Specify a unique key or combination of fields to prevent duplications
                unique_key = {'filename': base_filename}
                # pay attention
                # Update the collection with upsert option to prevent duplications
                collection.update_one(unique_key, {'$set': json_data}, upsert=True)

    client.close()

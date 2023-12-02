from pymongo import MongoClient

def query_slice(db_name, collection_name, gte_value, lte_value):
    # Swap values if gte_value is greater than lte_value
    if gte_value > lte_value:
        gte_value, lte_value = lte_value, gte_value

    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client[db_name][collection_name].aggregate([
        {
            '$match': {
                'ATLAS3D.Slice.ZIndex': {
                    '$gte': gte_value,
                    '$lte': lte_value
                }
            }
        }
    ])
    result_list = list(result_cursor)
    return result_list

def query_zpos(db_name, collection_name, gte_value, lte_value):
    # Swap values if gte_value is greater than lte_value
    if gte_value > lte_value:
        gte_value, lte_value = lte_value, gte_value

    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client[db_name][collection_name].aggregate([
        {
            '$match': {
                'ATLAS3D.Slice.ZIndex': {
                    '$gte': gte_value,
                    '$lte': lte_value
                }
            }
        }, {
            '$project': {
                'ATLAS3D.Slice.ZPos': 1
            }
        }
    ])
    result_list = list(result_cursor)
    return result_list

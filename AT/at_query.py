#This script shows two examples of queries
#More queries can designed using this script as a template

from pymongo import MongoClient

#  QUERY #1
def RowCol(db_name,collection_name, row, column):
    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client[db_name][collection_name].aggregate([
        {
            '$match': {
                'MosaicInfo.Row': row,
                'MosaicInfo.Col': column
            }
        }

    ])

    result_list = list(result_cursor)
    return result_list

# QUERY #2 MOSAIC INFO AND TILE HISTORY
def mosaic(db_name,collection_name, row, column):
    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client[db_name][collection_name].aggregate([
    {
        '$match': {
            'MosaicInfo.Row': row,
            'MosaicInfo.Col': column
        }
    }, {
        '$project': {
            'MosaicInfo': 1
        }
    }
])

    result_list = list(result_cursor)
    return result_list


def tileposition(db_name, collection_name, row, column):


    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client[db_name][collection_name].aggregate([
        {
            '$match': {
                'MosaicInfo.Row': row,
                'MosaicInfo.Col': column
            }
        }, {
            '$project': {
                'TilePositionHistory': 1
            }
        }
    ])
    result_list = list(result_cursor)
    return result_list


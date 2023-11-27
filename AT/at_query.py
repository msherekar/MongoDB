from pymongo import MongoClient

#  QUERY #1
def RowCol(collection_name, row, column):
    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client['AT'][collection_name].aggregate([
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
def mosaic(collection_name, row, column):
    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client['AT']['2023_11_23'].aggregate([
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


def tileposition(collection_name, row, column):


    client = MongoClient('mongodb://localhost:27017/')
    result_cursor = client['AT']['2023_11_23'].aggregate([
        {
            '$match': {
                'MosaicInfo.Row': 2,
                'MosaicInfo.Col': 9
            }
        }, {
            '$project': {
                'TilePositionHistory': 1
            }
        }
    ])
    result_list = list(result_cursor)
    return result_list


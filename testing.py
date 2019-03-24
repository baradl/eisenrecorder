"""
Script to set up easily everything to test functions.
"""

import connect
import request

import converter as conv
import helper as he



def create(db = "TrainingLogData", col = "empty"):
    client = connect.connect_to_client()
    db = client[db]
    if col != "empty":
        col = db [col]
        return db,col
    return db
    
    


def find(col, day):
    return request.find_session(col,day)


db = create()
    
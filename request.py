"""
Collection of functions that interact with the database.
"""

import helper as he
import printer
import checker
import updater


TYPES = ["off", "run", "SQ", "DL", "BP", "UB", "LB"]


###############################################################################
"""
Creates a dictionary that shall be later incorporated into the db. Consists of 
day, workout type, exercises and comments regarding the session.
"""

def construct_dict_session(day, workout_type, exercises = [], comments= ""):
    global TYPES
    assert workout_type in TYPES
    
    #if type(day) == int: day = str(day)
    doc = {"day": day, "type": workout_type}
    
    if workout_type == "run": doc.update({"run": exercises})
    
    elif workout_type != "off": 
        doc.update({ "amount of exercises": len(exercises)})
        for i in range(len(exercises)):
            doc.update({"exercise"+str(i+1): exercises[i]})
        exlist = []
        for j in range(len(exercises)):
            exercise = exercises[j]
            exlist.append(exercise[0])
        doc.update({"exercise list": exlist})
    
    doc.update({"comments": comments})
    return doc

###############################################################################

"""
Inserts the above described dictionary into a given collection.
"""
def insert_session(col, dic):
    assert type(col) is not str
    col.insert_one(dic)

###############################################################################

"""
Returns session of a given day.
"""
def find_session(col, day):
    #if type(day) == int: day = str(day)
    cursor = col.find()
    for document in cursor:
        if document["day"] == day:
            return document

###############################################################################

"""
Returns session of a given date.
"""
def find_session_by_date(col, date):
    consday = he.get_day_in_year(date)
    return find_session(col, consday)
    
        
###############################################################################

"""
Deletes session of a given day.
"""
def delete_session(col, day):
    query = { "day": day }
    col.delete_one(query)

###############################################################################
    
# =============================================================================
# """
# Creates a copy of a given collection.
# """
# def create_copy(col, db):
#     name = col.name + "_copy"
#     new = name
#     i = 1
#     while checker.check_col_exist(db, db[name]):
#         new = name + str(i)
#         i += 1
#     copy = db[new]
#     cursor = col.find()
#     for document in cursor:
#         copy.insert_one(document)
#     return copy
# =============================================================================
       
        
###############################################################################
    
    

    
import helper as he
import printer
import checker
import updater


TYPES = ["off", "run", "SQ", "DL", "BP", "UB", "LB"]



"""
insert: Name Collection, Tag, Art der Session, Übungen/Laufergebnisse
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

def insert_session(col, dic):
    assert type(col) is not str
    col.insert_one(dic)



def find_session(col, day):
    #if type(day) == int: day = str(day)
    cursor = col.find()
    for document in cursor:
        if document["day"] == day:
            return document
        


def delete_session(col, day):
    cursor = col.find()
    query = { "day": day }
    col.delete_one(query)


def create_copy(col, db):
    name = col.name + "_copy"
    new = name
    i = 1
    while checker.check_col_exist(db, db[name]):
        new = name + str(i)
        i += 1
    copy = db[new]
    cursor = col.find()
    for document in cursor:
        copy.insert_one(document)
    return copy
        
                

              
        
###############################################################################
    
    

    
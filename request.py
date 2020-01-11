from utils import helper as he
from crud import printer
from utils import checker
from crud import updater
import time

TYPES = ["off", "run", "hike", "SQ", "DL", "BP", "UB", "LB", "cardio"]

def construct_dict_session(day, workout_type, exercises = [], comments= ""):
    global TYPES
    assert workout_type in TYPES
    
    #if type(day) == int: day = str(day)
    doc = {"day": day, "type": workout_type}
    
    if workout_type == "run": doc.update({"run": exercises})
    
    elif workout_type == "hike": doc.update({"hike": exercises})
    
    elif workout_type == "cardio": doc.update({"run": exercises[0], "circuit": exercises[1]})

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
    cursor = col.find().sort("day")
    found = []
    for document in cursor:
        if document["day"] == day: found.append(document)
        if document["day"] > day: break    
    return found


def find_session_by_date(col, date):
    consday = he.get_day_in_year(date)
    return find_session(col, consday)
    
        
def delete_session(col, day):
    query = {"day": day}
    col.delete_one(query)
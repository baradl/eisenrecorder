"""
Collection of filters which prepare for statistical analysis of the bulk of 
workouts
"""

import helper as he

def filter_type(db, session_type):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    
    if type(session_type) == str:
        session_type = [session_type]
    
    for doc in cursor:
        if doc["type"] in session_type:
            filtered.append(doc)
            
    return filtered


def filter_consecutive_days(db, start, end):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    
    if type(start) == str and len(start) > 3:
        start = he.get_day_in_year(start)
    if type(end) == str and len(end) > 3:
        end = he.get_day_in_year(end)
    
    
    for doc in cursor:
        day = doc["day"]
        if day >= start and day <= end:
            filtered.append(doc)
    
    return filtered


def filter_days(db, day_list):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    
    for doc in cursor:
        if doc["day"] in day_list:
            filtered.append(doc)
            
    return filtered


def filter_exercise(db, exercise):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    days = []
    
    for doc in cursor:
        if doc["type"] != "off" and doc["type"] != "run":
            if exercise in doc["exercise list"]:
                exercise_as_list, day = he.get_exercise(doc, exercise)
                days.append(day)
                filtered.append(exercise_as_list)
            
    return filtered, days
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
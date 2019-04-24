"""
Collection of several functions that print a session.
"""

import helper as he
import pymongo as pm
import converter as conv

###############################################################################

def print_session(doc):
    print(he.indent())
    #print("ID:", doc["_id"])
    day = doc["day"]
    
    assert type(day) == int
    
    day = conv.convert_int_todate(day)
    
    print("Date:" + day)
    print("Type:", doc["type"])
    
    if doc["type"] != "off":    
        
        if doc["type"] == "run":
            run = doc["run"]
            print("Distance:", run[0], "km")
            print("Durationen: " + conv.convert_float_totime(run[1]))
            print("average Pace: " + conv.convert_float_totime(run[2]))
        
        else:
            n   = doc["amount of exercises"]
            print("Amount of exercises:", n)
            print("List of exercises:", end = " ")
            ex = doc["exercise list"]
            for i in range(n-1):
                print(ex[i], ",", end = " ")
            print(ex[n-1])
            for i in range(n):        
                print_exercise(doc["exercise" + str(i+1)])
    
    if len(doc["comments"]) > 3: print("Comments: " + doc["comments"])
    print(he.indent())

###############################################################################
    
def print_exercise(exercise, date = False):
    
    if not date: name = exercise[0]
    else: name = date
    #Type 1 exercise
    if len(exercise) == 4:
        sets     = exercise[1]
        reps     = exercise[2]
        weight   = exercise[3]
        print(name,": ", sets, "x", reps, "x", weight)
    else:
        print(name, ": ", end  =  " "),
        reps = exercise[1]
        weight = exercise[2]
        assert len(reps) == len(weight)
        extype = get_ex_type(reps, weight)
        
        if extype == 2: print_ex_type2(reps, weight)
        elif extype == 3: print_ex_type3(reps, weight)
        elif extype == 4: print_ex_type4(reps, weight)

"""
type1: sets x reps x weight
type2: reps x weight, reps x weight,... (inequal weight or reps)
type3: sets1 x reps1 x weight1, sets2 x reps2 x weight2,... (sets > 1)
type4: all reps equal but weight is not: reps x weight1, weight2,...

"""
###############################################################################       

def print_ex_type2(reps, weight):
    print(reps[0], "x", weight[0], end = " ")
    for i in range(1,len(reps)):
        print(", ", reps[i], "x", weight[i], end = " ")
    print(" ")

###############################################################################
    
def print_ex_type3(reps, weight):
    reps_div = he.divide_int_list(reps)
    weight_div = he.divide_int_list(weight)
    m_ = len(reps_div[0])
    n_ = len(weight_div[0])
    if m_ > n_:
        if n_ != 1: print(n_,"x", reps_div[0][0], "x",weight_div[0][0] , end = " ")
        else: print(reps_div[0][0], "x",weight_div[0][0] , end = " ") 
        weight_div.remove(weight_div[0])
        he.delete_ints(reps_div[0], reps_div[0][0], n_)
    elif m_ < n_:
        if m_ != 1: print(m_,"x", reps_div[0][0], "x",weight_div[0][0] , end = " ")
        else: print(reps_div[0][0], "x",weight_div[0][0] , end = " ")  
        reps_div.remove(reps_div[0])
        he.delete_ints(weight_div[0], weight_div[0][0], m_)
    else:
        print(m_,"x", reps_div[0][0], "x",weight_div[0][0] , end = " ")
        reps_div.remove(reps_div[0])
        weight_div.remove(weight_div[0])
        
    while reps_div != [] and weight_div != []:
        m_ = len(reps_div[0])
        n_ = len(weight_div[0])
        if m_ > n_:
            if n_ != 1: print(",",n_,"x", reps_div[0][0], "x",weight_div[0][0] , end = " ")
            else: print(",", reps_div[0][0], "x",weight_div[0][0] , end = " ")
            weight_div.remove(weight_div[0])
            he.delete_ints(reps_div[0], reps_div[0][0], n_)
        elif m_ < n_:
            if m_ != 1: print(",",m_,"x", reps_div[0][0], "x",weight_div[0][0] , end = " ")
            else: print(",", reps_div[0][0], "x",weight_div[0][0] , end = " ")
            reps_div.remove(reps_div[0])
            he.delete_ints(weight_div[0], weight_div[0][0], m_)
        else:
            if m_ != 1: print(",", m_,"x", reps_div[0][0], "x",weight_div[0][0] , end = " ")
            else: print(",", reps_div[0][0], "x",weight_div[0][0] , end = " ")
            reps_div.remove(reps_div[0])
            weight_div.remove(weight_div[0])
    print(" ")

###############################################################################

def print_ex_type4(reps, weight):
    print( reps[0] , "x" ,weight[0], end= " ")
    for i in range(1,len(weight)):
        print(",", weight[i], end = " ")
    print(" ")
"""
type1: sets x reps x weight
type2: reps x weight, reps x weight,... (inequal weight and reps)
type3: sets1 x reps1 x weight1, sets2 x reps2 x weight2,... (sets > 1)
type4: all reps equal but weight is not: reps x weight1, weight2,...

"""

###############################################################################
def get_ex_type(reps, weight):
    reps_div     = he.divide_int_list(reps)
    weight_div   = he.divide_int_list(weight)
    if len(reps_div) == len(reps) and len(weight_div) == len(weight): 
        return 2
    if len(reps_div) == 1 and len(weight_div) != 1 and len(weight_div) > len(weight)/2: 
        return 4
    return 3
    
# =============================================================================
#         for j in range(m-1):
#             print(reps[j], "x", weight[j], ", ", end = " "),
#         print(reps[m-1], "x", weight[m-1])
# =============================================================================
        
###############################################################################
        
def print_collection(col):
    if type(col) is pm.cursor.Cursor:
        for document in col:
            print_session(document)
    else: 
        cursor = col.find()
        print("Collection: ", col.name)
        for document in cursor:
            print_session(document)

###############################################################################
def print_days(col, days, range = True):
    cursor = col.find().sort("day")
    if range:
        for document in cursor:
            if document["day"] >= days[0] and document["day"] >= days[1]:
                print_session(document)
    else:
        for document in cursor:
            if document["day"] in days:
                print_session(document)
                

###############################################################################
"""
Prints sorted version of given collection. Problems with returning a sorted
collection because .sort() returns type pm.cursor.Cursor and not a collection.
Trying to copy each document in new collection and dropping old one failed
because of renaming new one.
"""           
def print_sort_col(col, by = "day"):
    cursor = col.find().sort(by)
    for document in cursor:
        print_session(document)
        
###############################################################################


def print_allsessions(db, days = "all"):
    col = db["AllSessions"]
    
    if days == "all":
        print_sort_col(col)
    
    else:
        for doc in col.find().sort("day"):
            if doc["day"] >= days[0] and doc["day"] <= days[1]:
                print_session(doc)


###############################################################################

def print_allsessions_type(db, session_type):
    col = db["AllSessions"]
    for doc in col.find():
        if doc["type"] == session_type:
            print_session(doc)


###############################################################################
            
            
def print_filter(doc_list):
    for doc in doc_list:
        print_session(doc)





















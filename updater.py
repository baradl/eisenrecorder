"""
Collection of update functions. One can update the day, type, comments of session.
In addition one can change exercises.
"""

import checker
###############################################################################
"""Updater"""               
                
def update_exercise(doc, newexercise, col):
    assert doc["type"] != "off"
    if doc["type"] != "run":
        exercises = doc["exercise list"]
        if newexercise[0] in exercises: 
            ex_num = exercises.index(newexercise[0])
            new = "exercise" + str(ex_num + 1)
            
            doc[new] = newexercise
            
        else:
            ex_num = len(exercises)
            exercises.append(newexercise[0])
            new = "exercise" + str(ex_num + 1)
            doc.update({new: newexercise})
            doc["amount of exercises"] += 1
            checker.check_exlist(doc)
    
    else:
        doc["run"] = newexercise
    col.save(doc)
    
###############################################################################      
def update_day(doc, newday ,col):
       
    doc["day"] = newday
    col.save(doc)

###############################################################################
def update_type(doc, newtype, col):  
    if doc["type"] == "off" and newtype != "off":
        doc.update({"exercise list": []})             
    
    doc["type"] = newtype
    col.save(doc)

###############################################################################
def update_comments(doc, newcomment, col):
    doc.update({"comments": newcomment})
    col.save(doc)
    


# =============================================================================
# def update(doc, new, col):
#     typ = type(new)
#     global TYPES
#     
#     if typ == str:
#         if typ in TYPES: kind = "type"
#         elif len(new) == 2: kind = "day"
#         
#     elif typ == list: kind = "exercise"
#     else: 
#         print("No valid input.")
#         raise SystemExit
#         
#     
#     if kind == "exercise": 
#         assert len(new) <= 4
#         assert len(new) >= 3
#         update_exercise(doc, new,col)
#     elif kind == "type":
#         update_type(doc, new,col)
#     elif kind == "day": 
#         update_day(doc, new,col)
# =============================================================================
    


###############################################################################
"""
Delete Exercises of a given document.
"""

def delete_exercise(doc, ex_list):
    
    if type(ex_list) == str:
        ex = []
        ex.append(ex_list)
        ex_list = ex
    assert type(ex_list) == list
    exercises = doc["exercise list"]
    for e in ex_list:
        if e not in exercises: ex_list.remove(e)
    n_ex = len(exercises)
    for i in range(n_ex):
        if exercises[i] in ex_list:
            doc.pop("exercise" + str(i+1))
            for j in range(i, n_ex - 1):
                doc["exercise" + str(j+1)] = doc["exercise" + str(j+2)]
            i -= 1
    k = 0
    n_list = len(ex_list)
    while k < n_list:
        doc.pop("exercise" + str(n_ex - k))
        k += 1
    doc["amount of exercises"] = len(exercises) - len(ex_list)
    checker.check_exlist(doc)
           



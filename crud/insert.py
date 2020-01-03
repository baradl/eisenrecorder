import request as re
from utils import helper as he
from parsing import converter as conv
from utils import check
from crud import printer

from menu import menu
from cache import cache







###############################################################################

"""
User menu to insert a session into the db.
"""
def insert_strength(db):    
    
    col = db["AllSessions"]
    
    print(he.indent())
    
    
    dec = input("Current month and year [y/n]: ")
    if dec == "y": 
        year = str(he.year_now())
        month = str(conv.convert_month_to_int(str(he.month_now())))
    else:
        year = input("Year: ")
        month = input("Month: ")
        month = str(conv.convert_month_to_int(month))
        
    
    day = input("Day: ")
    day = check.check_day(day)
    
    if len(day) == 1: day = "0" + day
    if len(month) == 1: month = "0" + month
    if len(year) ==2: year = "20" + year
    
    date = day + "." + month + "." + year
    
    cons_day = he.get_day_in_year(date)
    
    if re.checker.check_doc_exist(db, col, cons_day):
        doc = re.find_session(col, cons_day)
        printer.print_session(doc[0])
        dec = input("Day already exists. Change day [y/n]: ")
    
        if dec == "y": 
            insert_strength(db)
        
                
   
    workout_type = input("workout type: ")
    exercises = []
    try:
        assert workout_type != "off" and workout_type != "run"
    except:
        print("Type not accepted")
        insert_strength(db)
        
    while True:
        exercise = input("Exercise: ")
        if len(exercise) < 4: break
        exercise = conv.convert_input(exercise)
        exercises.append(exercise)
    
        
    comment_ = input("Any comments regarding the session: ")
    if len(comment_) < 3: comment_ = ""
        
    
    dic = re.construct_dict_session(cons_day, workout_type, exercises, comment_)
    
    print(he.indent())  
    print("Insert following session:")
    printer.print_session(dic)
    print(he.indent())

    decision = input("Correct [y/n]: ")
    if decision == "y": re.insert_session(col, dic)
    else: insert_strength(db)
    
    decision = input("Insert another session [y/n]: ")
    if decision == "y": insert_strength(db)
    


       
###############################################################################



def insert_run(db):    
    
    col = db["AllSessions"]
    
    print(he.indent())
    
    
    dec = input("Current month and year [y/n]: ")
    if dec == "y": 
        year = str(he.year_now())
        month = str(conv.convert_month_to_int(str(he.month_now())))
    else:
        year = input("Year: ")
        month = input("Month: ")
        month = str(conv.convert_month_to_int(month))
        
    
    day = input("Day: ")
    day = check.check_day(day)
    
    if len(day) == 1: day = "0" + day
    if len(month) == 1: month = "0" + month
    if len(year) ==2: year = "20" + year
    
    date = day + "." + month + "." + year
    
    cons_day = he.get_day_in_year(date)
    
    if re.checker.check_doc_exist(db, col, cons_day):
        doc = re.find_session(col, cons_day)
        printer.print_session(doc[0])
        dec = input("Day already exists. Change day [y/n]: ")
        
        if dec == "y": 
            insert_run(db)
        
                
   
    workout_type = "run"

    stats = input("Distance in km and time in minutes (dis time): ")
    run = conv.convert_run(stats)
    exercises = run
        
    comment_ = input("Any comments regarding the session: ")
    if len(comment_) < 3: comment_ = ""
        
    
    dic = re.construct_dict_session(cons_day, workout_type, exercises, comment_)
    print(he.indent())
    
    printer.print_session(dic)
    
    print(he.indent())
    decision = input("Correct [y/n]: ")
    if decision == "y": re.insert_session(col, dic)
    else: insert_run(db)
    
    decision = input("Insert another run [y/n]: ")
    if decision == "y": insert_run(db)


###############################################################################

def insert_off(db):    
    
    col = db["AllSessions"]
    
    print(he.indent())
     
    dec = input("Current month and year [y/n]: ")
    if dec == "y": 
        year = str(he.year_now())
        month = str(conv.convert_month_to_int(str(he.month_now())))
    else:
        year = input("Year: ")
        month = input("Month: ")
        month = str(conv.convert_month_to_int(month))
        
    
    day = input("Day: ")
    day = check.check_day(day)
    
    if len(day) == 1: day = "0" + day
    if len(month) == 1: month = "0" + month
    if len(year) ==2: year = "20" + year
    
    date = day + "." + month + "." + year
    
    cons_day = he.get_day_in_year(date)
    
    if re.checker.check_doc_exist(db, col, cons_day):
        doc = re.find_session(col, cons_day)
        printer.print_session(doc)
        dec = input("Day already exists. Change day [y/n]: ")

        if dec == "y": 
            insert_off(db)
        
                   
    workout_type = "off"
        
    comment_ = input("Any comments regarding the session: ")
    if len(comment_) < 3: comment_ = ""
        
    
    dic = re.construct_dict_session(cons_day, workout_type, comment_)
    print(he.indent())
    
    printer.print_session(dic)
    
    print(he.indent())
    
    decision = input("Correct [y/n]: ")
    if decision == "y": re.insert_session(col, dic)
    else: insert_off(db)
    
    decision = input("Insert another off day [y/n]: ")
    if decision == "y": insert_off(db)    


###############################################################################
    
def insert_hike(db):
    col = db["AllSessions"]
    
    print(he.indent())
     
    dec = input("Current month and year [y/n]: ")
    if dec == "y": 
        year = str(he.year_now())
        month = str(conv.convert_month_to_int(str(he.month_now())))
    else:
        year = input("Year: ")
        month = input("Month: ")
        month = str(conv.convert_month_to_int(month))
        
    
    day = input("Day: ")
    day = check.check_day(day)
    
    if len(day) == 1: day = "0" + day
    if len(month) == 1: month = "0" + month
    if len(year) ==2: year = "20" + year
    
    date = day + "." + month + "." + year
    
    cons_day = he.get_day_in_year(date)
    
    if re.checker.check_doc_exist(db, col, cons_day):
        doc = re.find_session(col, cons_day)
        printer.print_session(doc)
        dec = input("Day already exists. Change day [y/n]: ")

        if dec == "y": 
            insert_hike(db)
                       
    workout_type = "hike"
    
    dis = float(input("Distance [km]: "))
    height = float(input("Height meter: "))
    minutes, seconds = conv.convert_time_tofloat(input("Time: "))
    
    time = minutes + seconds/60
    
    exercises = [dis, height, time]
    
    comment_ = input("Any comments regarding the session: ")
    if len(comment_) < 3: comment_ = ""
        
    dic = re.construct_dict_session(cons_day, workout_type, exercises, comment_)
    print(he.indent())
    
    printer.print_session(dic)
    
    print(he.indent())
    
    decision = input("Correct [y/n]: ")
    if decision == "y": re.insert_session(col, dic)
    else: insert_hike(db)
    
    decision = input("Insert another hike [y/n]: ")
    if decision == "y": insert_hike(db)
# =============================================================================
# """
# Inserts all entries of all collections into the collection 'AllSessions'. Nothing
# if inserted twice. If entry already exists it is skipped.
# """
# 
# def insert_in_all(db):
#     col_all = db["AllSessions"]
#     
#     
#     list_col = db.list_collection_names()
#     if "AllSessions" in list_col:
#         list_col.remove("AllSessions")
#     for col_name in list_col:
#         col = db[col_name]
#         
#         for document in col.find().sort("day"):
#             alldays = he.get_days_col(col_all)
#             [multi, missing]  = check.check_int_list(alldays)
#             if len(missing) == 0:
#                 if re.checker.alreadyExists(document["_id"], col_all): 
#                     continue
#                 else:
#                     document["day"] = max(alldays) + 1
#                     col_all.insert_one(document)
#             else: 
#                 print("These days are missing: ", missing)
#                 print("Insert these manually before automated insertion.")      
# =============================================================================
    
    
    

###############################################################################
        
        





    
    
    
    
    
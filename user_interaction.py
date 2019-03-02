import request as re
import helper as he
from helper import converter as conv
from helper import check
import menu
import cache







###############################################################################

    
def user_insert(db, col = True):    
    
    print(he.indent())
    if col == True: 
        col = input("Collection: ")
        col = conv.convert_col_input(col)
        #if he.is_host_local(db.client): col = col + "_cache"
        day = input("Day: ")
        day = check.check_day(day)
        while re.checker.check_doc_exist(db, db[col], day):
            x = input("Day already exists for this month. Change day? ")
            if x == "yes": 
                day = input("New day: ")
                day = check.check_day(day)
    else: 
        if type(col) != str: col = col.name
        day = input("Day: ")
        day = check.check_day(day)
    workout_type = input("workout type: ")
    exercises = []
    if workout_type != "off" and workout_type != "run":
        print("'name sets reps weight' or 'name reps weight'")
        see_abb = input("See abbreviation? ")
        if see_abb == "yes": he.abbreviation()
        while True:
            exercise = input("Exercise: ")
            if len(exercise) < 4: break
            exercise = conv.convert_input(exercise)
            exercises.append(exercise)
    elif workout_type == "run": 
        stats = input("Distance in km and time in minutes (dis time): ")
        run = conv.convert_run(stats)
        exercises.append(run)
        
    comment_ = input("Any comments regarding the session: ")
    if len(comment_) < 3: comment_ = ""
        
    
    dic = re.construct_dict_session(day,workout_type, exercises, comment_)
    print(he.indent())
    print("Insert following session:")
    print("Collection:",col)
    print("Day:", day)
    print("Type:", workout_type)
    if workout_type != "off" and workout_type != "run":
        print("Exercise list:", dic["exercise list"])
    
    print(he.indent())
    decision = input("Correct? ")
    if decision == "yes": re.insert_session(db[col], dic)
    else: user_insert(db)
    
    decision = input("Insert another session? ")
    if decision != "no":user_insert(db)
    


       
###############################################################################



def insert_in_all(db):
    col_all = db["AllSessions"]
    
    
    list_col = db.list_collection_names()
    if "AllSessions" in list_col:
        list_col.remove("AllSessions")
    for col_name in list_col:
        col = db[col_name]
        
        for document in col.find().sort("day"):
            alldays = he.get_days_col(col_all)
            [multi, missing]  = check.check_int_list(alldays)
            if len(missing) == 0:
                if re.checker.alreadyExists(document["_id"], col_all): 
                    continue
                else:
                    document["day"] = max(alldays) + 1
                    col_all.insert_one(document)
            else: 
                print("These days are missing: ", missing)
                print("Insert these manually before automated insertion.")      
    
    
    

###############################################################################
        
        





    
    
    
    
    
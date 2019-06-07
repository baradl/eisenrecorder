"""
Collection of functions to work with the cache.
"""

###############################################################################

import helper as he
import request as re
import checker
from helper import converter as conv
from helper import check
import pickle, glob, os
import menu

###############################################################################

CACHE_DIR = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/cached_sessions/"



"""
Inserts a session into the cache. Very similar to insertion into DB. The inserted
session is afterwards pickled and saved locally. The file name is the number of
consecutive days (beginning at 01.01.2019) corresponding to the date of interest.
"""
def insert_cache():   
    while True:
        dec = input("Current year [y/n]: ")
        if dec == "y": year = "2019"
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
            
        dic = re.construct_dict_session(cons_day,workout_type, exercises, comment_)
        print(he.indent())
        print("Insert following session:")
        print("Date: " + date)
        print("Type:", workout_type)
        if workout_type != "off" and workout_type != "run":
            print("Exercise list:", dic["exercise list"])
        
        print(he.indent())
        decision = input("Correct [y/n]: ")
        if decision == "y": 
            save_cache_entry(dic)
        else: continue
        
        decision = input("Session cached. Insert another one [y/n]: ")
        if decision != "y": break




###############################################################################


"""
Saves the date (meaning the dictionary corresponding to a session) as a pickled
file into a folder prepared beforehand.
"""
def save_cache_entry(data):
    day = data["day"]
    global CACHE_DIR
    
    filepath = CACHE_DIR
    
    filepath += str(day)
    if find_session(day) is not None:
        filepath += "(1)"
    
    filepath += ".txt"
    
    pickle.dump(data,open(filepath, "wb"))        





###############################################################################
    
    
    
"""
Takes all files in the cache directory, unpickles and uploads them into the
collection "AllSessions". Before the upload is finalized it is verified that 
no file corresponding to the same date already exists. If that is the case the
user has to confirm the upload (two workouts in one day are possible).

Since the online client is just used for this function it is closed afterwards.
"""       
def upload_cache():
    import connect as con
    global CACHE_DIR
    client = con.connect_to_client()
    db = client["TrainingLogData"]
    col = db["AllSessions"]
    directory = CACHE_DIR
    os.chdir(directory)
    
    for file_ in glob.glob("*.txt"):
        filepath = directory + file_
        doc = pickle.load(open(filepath,"rb"))
        day = doc["day"]
        
        if checker.check_doc_exist(db, col, day):
            print("Day", day, "already exists")
            dec = input("Insert anyway [y/n]: ")
            if dec == "y": re.insert_session(col, doc)
            else: continue
        else: re.insert_session(col, doc)
    client.close()
    #delete_cache("all")



###############################################################################

        

"""
Prints out a list of dates of all cached sessions.
"""
def see_cache():
    print(he.indent())
    global CACHE_DIR
    directory = CACHE_DIR
    os.chdir(directory)
    
    print("Dates with cached session:")
    for file_ in glob.glob("*.txt"):
        day = file_.replace(".txt", "")
        day = day.replace("(1)", "")
        
        
        day = int(day)
        
        date = conv.convert_int_todate(day)
        
        print(date)


###############################################################################
        
        
        
"""
Deletes one or all cached sessions. If a session shall be deleted that is not
existent the user goes back to the start menu.
"""
def delete_cache(day):
    global CACHE_DIR
    
    if is_empty(): 
        print("Cache is currently empty. Closing")
        menu.menu_cache()
    directory = CACHE_DIR
    os.chdir(directory)
    
    if day == "all":
        for file_ in glob.glob("*.txt"):
            os.remove(file_)
    
    else:
        file = find_session(day)
        if file == None:
            print("Date not found. Going back to main menu.")
            menu.user_start()
        else:
            for file_ in file:
                os.remove(directory + file_)
        
###############################################################################
        
        
"""
Returns the list of pickled files that contain the day and None if such a day 
does not exists.
"""            
def find_session(day):
    global CACHE_DIR
    assert type(day) == int
    
    directory = CACHE_DIR
    os.chdir(directory)
    files = glob.glob("*.txt")
    
    for file_ in files:
        file_ = file_.replace(".txt","")
    
    findings = he.find_substring_in_stringlist(files, str(day))
    
    if findings == []: return None
    else: return findings
    


###############################################################################
    
    
    
"""
Checks if cache is currently empty. Returns boolean.
"""    
def is_empty():
    global CACHE_DIR
    directory = CACHE_DIR
    os.chdir(directory)
    files = glob.glob("*.txt")
    
    if files == []: return True
    else: return False 
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
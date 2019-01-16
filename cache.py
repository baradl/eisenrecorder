import helper as he
import request as re
import checker
from helper import converter as conv
from helper import check
import pickle, glob, os

###############################################################################


def insert_cache():   
    while True:
            month = input("Month: ")
            try: 
                month = int(month)
                month = str(month)
                month = he.check_day(month)
            except:
                month = conv.convert_month_to_int(month)
                month = check.check_day(str(month))
            month = month
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
            data = [month, dic]
            print(he.indent())
            print("Insert following session:")
            print("Collection:", month)
            print("Day:", day)
            print("Type:", workout_type)
            if workout_type != "off" and workout_type != "run":
                print("Exercise list:", dic["exercise list"])
            
            print(he.indent())
            decision = input("Correct? ")
            if decision == "yes": 
                year = "2019"
                directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/cached_sessions/"
                day = dic["day"]
                if find_session(day, month, year) is not None:
                    filepath = directory + day + month + year + "(1)"
                filepath = filepath + ".txt"
                pickle.dump(data,open(filepath, "wb"))
            else: continue
            
            decision = input("Session cached. Insert another one? ")
            if decision != "yes": break

###############################################################################
            
        
def upload_cache(db):
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/cached_sessions/"
    os.chdir(directory)
    
    for file_ in glob.glob("*.txt"):
        filepath = directory + file_
        item = pickle.load(open(filepath,"rb"))
        col_name = conv.convert_to_month(item[0])
        doc      = item[1]
        day = doc["day"]
        if checker.check_doc_exist(db, db[col_name], day):
            print("Day", day, "already exists in", col_name)
            dec = input("Insert anyway? ")
            if dec == "yes": re.insert_session(db[col_name], doc)
            else: continue
        else: re.insert_session(db[col_name], doc)
    
    delete_cache("all")
        

def see_cache():
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/cached_sessions/"
    os.chdir(directory)
    
    for file_ in glob.glob("*.txt"):
        name = file_.replace(".txt", "")
        if len(name) > 8: name = name[:8]
        day = name[:2]
        year = name[-4:]
        month = name.replace(day, "")
        month = month.replace(year, "")
        
        print(day + "." + month + "." + year)



def delete_cache(day, month = "", year = "2019"):
    
    
    
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/cached_sessions/"
    os.chdir(directory)
    
    if day == "all":
        for file_ in glob.glob("*.txt"):
            os.remove(file_)
    
    else:
        month = conv.convert_month_to_int(month)
        file = find_session(day, month, year)
        os.remove(directory + file)

            
"""
returns pickled file if day exists in cache and None if such a day does not 
exist
"""            
def find_session(day, month, year = "2019"):
    month = conv.convert_month_to_int(month)
    month = str(month)
    if len(month) == 1: month = "0" + month
    
    day = str(day)
    if len(day) == 1: day = "0" + day
    
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/cached_sessions/"
    os.chdir(directory)
    files = glob.glob("*.txt")
    
    for file_ in files:
        file_ = file_.replace(".txt","")
    
    findings = he.find_substring_in_stringlist(files, day+month+year)
    
    if findings == []: return None
    else: return findings
    


def is_empty():
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/cached_sessions/"
    os.chdir(directory)
    files = glob.glob("*.txt")
    
    if files == []: return True
    else: return False 
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
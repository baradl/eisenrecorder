import helper as he
from helper import converter as conv
import connect as con
import user_interaction as ui
import request as re
import cache
import printer

def user_start():
    if con.check_internet() and not cache.is_empty():
        decision = input("Cache can be uploaded. Confirm? ")
        if decision == "yes":
            cache.upload_cache()
    print(he.indent())
    print("1. Edit Sessions \n2. Edit Cache \n3. Backup")
    dec1 = input("\nChoose number or press enter for exit: ")
    
    if dec1 == "1":
        if con.check_internet():
            print("Connecting to online host.")
            print(he.indent())
            print("\n")
            client = con.connect_to_client()
            db = client["TrainingLogData"]
            user_menu(db)
        else:
            print("No network service. Going back to main menu")
            user_start()
    
    elif dec1 == "2": 
        menu_cache()
    elif dec1 == "3":
        backup_menu()
    
        
    else:
        print("Exit.")


###############################################################################

    




def user_choose_database(myclient):        
    print("List of databases:")
    print(myclient.list_database_names())
    print("\n")
    print("List of collections in TrainingLogData:")
    print(myclient["TrainingLogData"].list_collection_names())
    print("\n")
    x = input("Standard mode or test mode: ")
    
    if x == "test":
        x = input("Database to be referenced: ")
        db = myclient[x]
        print("Collections: ", db.list_collection_names())
        print(he.indent())
        #user_menu(db)
    else:
        print("Currently working on:",end = " ")
        current_month = conv.convert_to_month(he.month_now())
        current_year = str(he.year_now())
        print(current_month + current_year)
        db = myclient["TrainingLogData"]
        print(he.indent())
        #user_menu(db)

    user_menu(db)






###############################################################################


def user_menu(db):
    print("1. Insert a session \n2. Delete a session \n3. Edit a session \n4. See month/year/all")
    input_ = input("\nChoose number or press enter for exit: ")
    
    print(he.indent())
    if input_ == "1":
        print("Inserting one session.")
        ui.user_insert(db)
    
    elif input_ == "2":
        date = input("Date to delete (dd.mm.yy): ")
        [day, month, year] = conv.convert_date(date)
        col_name = conv.convert_to_month(month) + "20" + str(year)
        col = db[col_name]
        if len(str(day)) < 2: day = "0" + str(day)
        else: day = str(day) 
        session = re.find_session(col, day)
        re.printer.print_session(session)
        dec = input("Delete this session?\n")
        if dec == "yes": re.delete_session(col, day)
    
    elif input_ == "3":
        date = input("Date of session (dd.mm.yy): ")
        [day, month, year] = conv.convert_date(date)
        col_name = conv.convert_to_month(month) + "20" + str(year)
        col = db[col_name]
        if len(str(day)) == 1: day = "0" + str(day)
        else: day = str(day)
        session = re.find_session(col, day)
        re.printer.print_session(session)
        dec = input("Edit this this session? ")
        if dec == "yes": user_menu_edit(session, col)
        else: 
            print("No valid input. Going back to menu.")
            user_menu(db)
    
        
    elif input_ == "4":
        decision = input("What do you want to see [month/year/all]: ")
        
        menu_see(db,decision)
        
    else: 
        dec = input("Wrong number [y/n]: ")
        if dec == "y": user_menu(db)          
    
    print(he.indent())
    dec = input("Back to database menu [y/n]: ")
    if dec == "y": user_menu(db)
    
 
###############################################################################
    
    
    
def menu_see(db, decision):
    
    if decision == "month":
        date = input("mm.yyyy: ")
        [month, year] = date.split(".")
        
        if len(year) == 2: year = "20" + year
        
        month = conv.convert_month_to_int(month)
        
        monthly_days = he.monthly_days(int(year))
        
        days = [sum(monthly_days[:month-1])+1,sum(monthly_days[:month])]
        
        printer.print_allsessions(db, days)
    
    elif decision == "year":
        year = input("Which year would you like to see: ")
        
        year = int(year)
        days_in_year = 365
        
        if he.leap(year): days_in_year += 1
        
        consecutive_days = 0
        while year > 2019:
            consecutive_days += 365
            if he.leap(year): consecutive_days += 1
        
            year -= 1
        
        printer.print_allsessions(db, [consecutive_days + 1, consecutive_days 
                                       + days_in_year])
        
        
    elif decision == "all":
        printer.print_allsessions(db)
        
    else:
        print("No valid input. Closing.")
        
        
    
    
###############################################################################


def user_menu_edit(session, col):
    print(he.indent())
    print("1. Change day \n2. Change workout type \n3. Change/Add exercises \n4. Delete exercises \n5. Add/Change comment")
    dec = input("\nWhat shall be editted: ")
    
    print(he.indent())
    if dec == "1":
        newday = input("New day: ")
        re.updater.update_day(session, newday)
    elif dec == "2":
        oldtype = session["type"]
        newtype = input("New type: ")
        re.updater.update_type(session, newtype)
        if oldtype == "off":
            print("Insert the new exercises.")
            if newtype == "run":
                stats = input("Distance in km and time in minutes (dis time): ")
                run = conv.convert_run(stats)
                session.update({"run": run})
            else:
                print("Exercises either as 'name sets reps weight' or 'name reps weight'. In the latter seperate reps and weight by comma. Type 'no' if no more exercises shall be implemented.")
                exercises = []
                while True:
                    exercise = input("Exercise: ")
                    if len(exercise) < 4: break
                    exercise = he.convert_input(exercise)
                    exercises.append(exercise)
                for i in range(len(exercises)):
                    session.update({"exercise"+str(i+1): exercises[i]})
                exlist = []
                for j in range(len(exercises)):
                    exercise = exercises[j]
                    exlist.append(exercise[0])
                session.update({"exercise list": exlist})
        col.save(session)
    elif dec == "3":
        while True:
            new_ex = input("New exercise: ")
            if len(new_ex) < 4: break
            new_ex = conv.convert_input(new_ex)
            print(new_ex)
            re.updater.update_exercise(session, new_ex, col)
        
            
        
    elif dec == "4":
        ex = input("List exercises to be deleted: ")
        ex_list = ex.split()
        re.updater.delete_exercise(session, ex_list)
        
    elif dec == "5":
        newcomment = input("New comment: ")
        re.updater.update_comments(session, newcomment, col)
    else:
        dec = input("No valid input. Back to menu? ")
        if dec == "yes": user_menu_edit()
        else: raise SystemExit
    
    re.printer.print_session(session)
    dec = input("Back to database menu [y/n]: ")
    if dec == "y": user_menu(col.database)
        
            
 
###############################################################################
    
    
def menu_cache():
    import cache
    print("1. Insert into cache. \n2. Upload cache \n3. See all cache sessions \n4. Delete cached sessions")
    dec = input("\nChoose number or press enter for exit: ")
    
    if dec == "1":
        cache.insert_cache()           
        
    elif dec == "2":
        if con.check_internet():
            cache.upload_cache() 
        else:
            print("No network connection. Try later.")
    elif dec == "3":
        cache.see_cache()
    elif dec == "4":
        date = input("Type 'all' or specific date: ")
        
        try:
            date = conv.convert_date(date)
            cache.delete_cache(date)
        except: 
            cache.delete_cache(date)           
            
        
    else:
        print("Closing.")
        

###############################################################################        


def backup_menu():
    import backup
    print("1. Create backup \n2. See backup")
    decision = input("Choose number or press enter for exit: ")
    
    if decision == "1":
        host = con.connect_to_client()
        db = host["TrainingLogData"]
        col = db["AllSessions"]
        backup.create_backup(col)
        print("Backed it up.")
    elif decision == "2":
        backup.check_backup()
    else:
        print("Closing.")    
                
        
# =============================================================================
# ###############################################################################        
#             
# def user_menu_start():
#     print("Eisenrecorder started.")
#     print("1. Connection \n2. Syncronization")
#     dec1 = input("Choose number or press enter for exit.\n")
#     
#     if dec1 == "1" or dec1 == "2": 
#         print(he.indent())
#         return dec1
#         
#     else:
#         print("Exit.")
#         raise SystemExit
# 
# 
# 
# ###############################################################################   
#     
#     
#         
#         
# 
# def user_syncro_menu():
#     print("1. Upload \n2. Download")
#     dec3 = input("Upload or Download: ")
#     
#     if dec3 == "1": direction = "up"
#     elif dec3 == "2": direction = "down"
#     else: 
#         print("No valid input. Shutting down.")
#         raise SystemExit
#     print("1. Whole client \n2. Database \n3. Collection")
#     level = input("Syncronize which level: ")
#     
#     if level == "1": level = "clients"
#     elif level == "2": level = "db"
#     elif level == "3": level = "col"
#     else: 
#         print("No valid input. Shutting down.")
#         raise SystemExit
#     return [direction, level]
#  
#    
#     
# =============================================================================
    
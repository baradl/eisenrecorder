"""
Collection of menus used within the UI.
"""

import helper as he
from helper import converter as conv
import connect as con
import user_interaction as ui
import request as re
import cache
import printer
import filter
from datetime import datetime


###############################################################################

"""
Start menu. User can work on sessions, backup or cache.
"""

def user_start():
    if con.check_internet() and not cache.is_empty():
        print(he.indent())
        decision = input("Cache can be uploaded. Confirm [y/n]: ")
        if decision == "y":
            cache.upload_cache()
    print(he.indent())
    print("1. Edit Sessions \n2. Edit Cache \n3. Backup \n4. Session Prep \n5. Run Menu")
    dec1 = input("\nChoose number or press enter for exit: ")
    
    if dec1 == "1":
        if con.check_internet():
            print("Connecting to online host.")
            print(he.indent())
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
    elif dec1 == "4":
        if con.check_internet():
            print("Connecting to online host.")
            print(he.indent())
            client = con.connect_to_client()
            db = client["TrainingLogData"]
            prep_menu(db)
        else:
            print("No network service. Going back to main menu")
            user_start()
    elif dec1 == "5":
       if con.check_internet():
            print("Connecting to online host.")
            print(he.indent())
            client = con.connect_to_client()
            db = client["TrainingLogData"]
            run_menu(db)
       else:
            print("No network service. Going back to main menu")
            user_start()
        
        
    
        
    else:
        print("Exit.")


###############################################################################

    
# =============================================================================
# """
# User can choose between different databases to reference.
# """
# 
# 
# def user_choose_database(myclient):        
#     print("List of databases:")
#     print(myclient.list_database_names())
#     print("\n")
#     print("List of collections in TrainingLogData:")
#     print(myclient["TrainingLogData"].list_collection_names())
#     print("\n")
#     x = input("Standard mode or test mode: ")
#     
#     if x == "test":
#         x = input("Database to be referenced: ")
#         db = myclient[x]
#         print("Collections: ", db.list_collection_names())
#         print(he.indent())
#         #user_menu(db)
#     else:
#         print("Currently working on:",end = " ")
#         current_month = conv.convert_to_month(he.month_now())
#         current_year = str(he.year_now())
#         print(current_month + current_year)
#         db = myclient["TrainingLogData"]
#         print(he.indent())
#         #user_menu(db)
# 
#     user_menu(db)
# =============================================================================



###############################################################################


"""
When interacting with sessions the user can insert, edit and delete sessions. 
In addition one can print a single sessions, a month/year of sessions or all 
sessions.
"""

def user_menu(db):
    col = db["AllSessions"]
    print("1. Insert a session \n2. Delete a session \n3. Edit a session \n4. See single session \n5. See week/month/year/all")
    input_ = input("\nChoose number or press enter for exit: ")
    
    print(he.indent())
    if input_ == "1":
        print("Inserting one session.")
        print("'name sets reps weight' or 'name reps weight'")
        see_abb = input("See abbreviation [y/n]: ")
        if see_abb == "y": he.abbreviation()
        ui.user_insert(db)
    
    elif input_ == "2":
        date = input("Date to delete (dd.mm.yy): ")
        cons_day = he.get_day_in_year(date)
        
        session = re.find_session(col, cons_day)
        re.printer.print_session(session)
        dec = input("Delete this session [y/n]: ")
        if dec == "y": re.delete_session(col, cons_day)
    
    elif input_ == "3":
        date = input("Date to edit (dd.mm.yy): ")
        cons_day = he.get_day_in_year(date)
        
        session = re.find_session(col, cons_day)
        re.printer.print_session(session)
        dec = input("Edit this this session [y/n]: ")
        if dec == "y": user_menu_edit(session, col)
        else: 
            print("No valid input. Going back to menu.")
            user_menu(db)
    
    elif input_ == "4":
        date = input("Date of session (dd.mm.yy): ")
        cons_day = he.get_day_in_year(date)
        
        session = re.find_session(col, cons_day)
        re.printer.print_session(session)
        
    elif input_ == "5":
        decision = input("What do you want to see [week/month/year/all]: ")
        
        menu_see(db,decision)
        
    else: 
        dec = input("Wrong number [y/n]: ")
        if dec == "y": user_menu(db)          
    
    print(he.indent())
    dec = input("Back to database menu [y/n]: ")
    if dec == "y": user_menu(db)
    
 
###############################################################################
    
"""
Menu to let the user input the sessions one wants to print.
""" 
    
def menu_see(db, decision):
    
    if decision == "week":
        dec = input("Current week[y/n]: ")
        if dec == "y": 
            day = str(datetime.now().day)
            month = str(he.month_now())
            year = str(he.year_now())
            
            date = day + "." + month + "." + year
        else:
            date = input("Date in week of interest: ")
        
        [start, end] = he.get_week(date)
        
        doc_list = filter.filter_consecutive_days(db, start, end)
        
        printer.print_filter(doc_list)
    
    elif decision == "month":
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

"""
If a session shall be edited the user is guided via this menu. 
"""

def user_menu_edit(session, col):
    print(he.indent())
    print("1. Change day \n2. Change workout type \n3. Change/Add exercises \n4. Delete exercises \n5. Add/Change comment")
    dec = input("\nWhat shall be editted: ")
    
    print(he.indent())
    if dec == "1":
        newdate = input("New date (dd.mm.yy): ")
        newday = he.get_day_in_year(newdate)
        re.updater.update_day(session, newday, col)
    elif dec == "2":
        oldtype = session["type"]
        newtype = input("New type: ")
        re.updater.update_type(session, newtype, col)
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
        re.updater.delete_exercise(session, ex_list, col)
        
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

"""
Menu to guide user through cache option.
"""  
    
def menu_cache():
    import cache
    print("1. Insert cache \n2. Upload cache \n3. See cached sessions \n4. Delete cached sessions")
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
        date = input("['all'/'dd.mm.yy']: ")
        if date == "all":
            cache.delete_cache(date)
        else:
            day = he.get_day_in_year(date)
            cache.delete_cache(day)
            
        
    else:
        print("Closing.")
        

###############################################################################        

"""
Menu to guide the user through backup menu.
"""

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
                

###############################################################################
        
        
def prep_menu(db):
    import filter
    types = re.TYPES
    print("1. Print Session type \n2. Print Exercise \n3. Run Summary \n4. Other \n")
    decision = input("Choose number or press enter for exit: ")
    
    if decision == "1":
        while(True):
            type_ = input("Type: ")
            if type_ in types: break
            else: print("Selected type does not exist.")
        
        session_list = filter.filter_type(db, type_)
        
        printer.print_filter(session_list)
    
    elif decision == "2":
        exercise = input("Exercise to be listed: ")
        exercise_list, days = filter.filter_exercise(db, exercise)
        
        for i in range(len(days)):
            printer.print_exercise(exercise_list[i], 
                                   conv.convert_int_todate(days[i]))
    
    elif decision == "3":
        print("Not yet implemented")
    
    else:
        print("Closing.")
    

###############################################################################
        
def run_menu(db):
    print("1. Insert Run \n2. Summary \n")
    decision = input("Choose number or press enter for exit: ")
    
    if decision == "1":
        ui.insert_run(db)
    elif decision == "2":
        import summary
        print(he.indent())
        summary.summary_run(db)
        print(he.indent())
        dec = input("See specific week: ")
        
        try: 
            dec = int(dec)
            runs = summary.weekly_runs(db, dec + summary.START -1)
        
            printer.print_filter(runs)
            dec = input("Back to run menu [y/n]: ")
            if dec == "y": run_menu(db)
        
        except: 
            print("Closing")

        
    else: 
        dec = input("Back to run menu [y/n]: ")
        if dec == "y": run_menu(db)
        print("Closing")
        
    
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
    
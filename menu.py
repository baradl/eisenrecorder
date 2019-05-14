"""
Collection of menus used within the UI.
"""

import helper as he
from helper import converter as conv
import connect as con
import request as re
import cache
import printer
import submenu


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
    print("1. Strenght \n2. Run \n3. Off \n4. Cache \n5. Backup")
    dec1 = input("\nChoose number or press enter for exit: ")
    options = ["strength", "run", "off"]
    try:
        dec1 = int(dec1)
    except: 
        print("Closing")
        quit()
    
    
    
    
    if dec1 in [1,2,3]:
        if con.check_internet():
            print("Connecting to online host.")
            print(he.indent())
            client = con.connect_to_client()
            db = client["TrainingLogData"]
            print("Choose", options[dec1-1])
            session_menu(db, options[dec1-1])
        else:
            print("No network service. Going back to main menu")
            user_start()        
    elif dec1 == 4:
        menu_cache()
    elif dec1 == 5:
        backup_menu()
       
        
        
    
        
    else:
        print("Exit.")


###############################################################################



def session_menu(db, type_):
    print("1. Insert, change, delete a session \n2. Read session/week/month/year/all \n3. Analyze")    
    input_ = input("\nChoose number or press enter for exit: ")
    
    print(he.indent())
    
    options = ["strength", "run", "off"]
    assert type_.lower() in options
    
    if input_ == "1":
        decision = submenu.cud_actions()
        if decision == "1":
            submenu.insert(db, type_)
        elif decision == "2":
            submenu.edit(db, db["AllSessions"])
        elif decision == "3":
            date = input("Date to delete (dd.mm.yy): ")
            cons_day = he.get_day_in_year(date)
            
            col = db["AllSessions"]
            session = re.find_session(col, cons_day)
            re.printer.print_session(session)
            dec = input("Delete this session [y/n]: ")
            if dec == "y": re.delete_session(col, cons_day)
            
    elif input_ == "2":
        submenu.read(db, submenu.read_decision())
        
    elif input_ == "3":
        if options.index(type_) == 0:
            prep_menu(db)
        elif options.index(type_) == 1:
            import analyse_run as ar
            print(he.indent())
            ar.summary_run(db)
            print(he.indent())
            dec = input("See specific week: ")
            
            try: 
                dec = int(dec)
                runs = ar.weekly_runs(db, dec + ar.START -1)
            
                printer.print_filter(runs)
                dec = input("Back to run menu [y/n]: ")
                if dec == "y": session_menu(db, type_)
            
            except: 
                print("Closing")
        elif options.index(type_) == 2:
            import analyse_off as ao
            ao.summary_off(db)
        
    else:
        print("Closing")
        
        

# =============================================================================
# def strength_menu(db):
#     print("1. Insert, change, delete a session \n2. Read session/week/month/year/all \n3. Analyze")    
#     input_ = input("\nChoose number or press enter for exit: ")
#     
#     print(he.indent())
#     
#     if input_ == "1":
#         decision = submenu.cud_actions()
#         if decision == "1":
#             submenu.insert(db, "strength")
#         elif decision == "2":
#             submenu.edit(db, db["AllSessions"])
#         elif decision == "3":
#             date = input("Date to delete (dd.mm.yy): ")
#             cons_day = he.get_day_in_year(date)
#             
#             col = db["AllSessions"]
#             session = re.find_session(col, cons_day)
#             re.printer.print_session(session)
#             dec = input("Delete this session [y/n]: ")
#             if dec == "y": re.delete_session(col, cons_day)
#             
#     elif input_ == "2":
#         submenu.read(db, submenu.read_decision())
#         
#     elif input_ == "3":
#         prep_menu(db)
#     else:
#         print("Closing")
#         
#             
# def run_menu(db):
#     print("1. Insert, change, delete a run \n2. Read session/week/month/year/all \n3. Analyze")    
#     input_ = input("\nChoose number or press enter for exit: ")
#     
#     print(he.indent())
#     
#     if input_ == "1":
#         decision = submenu.cud_actions()
#         if decision == "1":
#             submenu.insert(db, "run")
#         elif decision == "2":
#             submenu.edit(db, db["AllSessions"])
#         elif decision == "3":
#             date = input("Date to delete (dd.mm.yy): ")
#             cons_day = he.get_day_in_year(date)
#             
#             col = db["AllSessions"]
#             session = re.find_session(col, cons_day)
#             re.printer.print_session(session)
#             dec = input("Delete this run [y/n]: ")
#             if dec == "y": re.delete_session(col, cons_day)
#             
#     elif input_ == "2":
#         submenu.read(db, submenu.read_decision())
#     elif input_ == "3":
#         import analyse_run as ar
#         print(he.indent())
#         ar.summary_run(db)
#         print(he.indent())
#         dec = input("See specific week: ")
#         
#         try: 
#             dec = int(dec)
#             runs = ar.weekly_runs(db, dec + ar.START -1)
#         
#             printer.print_filter(runs)
#             dec = input("Back to run menu [y/n]: ")
#             if dec == "y": run_menu(db)
#         
#         except: 
#             print("Closing")
# 
#         
#     else: 
#         dec = input("Back to run menu [y/n]: ")
#         if dec == "y": run_menu(db)
#         print("Closing")
#         
# 
# def off_menu(db):
#     print("1. Insert, change, delete a off day \n2. Read session/week/month/year/all \n3. Analyze")    
#     input_ = input("\nChoose number or press enter for exit: ")
#     
#     print(he.indent())
#     
#     if input_ == "1":
#         decision = submenu.cud_actions()
#         if decision == "1":
#             submenu.insert(db, "off")
#         elif decision == "2":
#             submenu.edit(db, db["AllSessions"])
#         elif decision == "3":
#             date = input("Date to delete (dd.mm.yy): ")
#             cons_day = he.get_day_in_year(date)
#             
#             col = db["AllSessions"]
#             session = re.find_session(col, cons_day)
#             re.printer.print_session(session)
#             dec = input("Delete this off day [y/n]: ")
#             if dec == "y": re.delete_session(col, cons_day)
#             
#     elif input_ == "2":
#         submenu.read(db, submenu.read_decision())
#     elif input_ == "3":
#         import analyse_off as ao
#         ao.summary_off(db)
# 
#         
#     else: 
#         dec = input("Back to run menu [y/n]: ")
#         if dec == "y": run_menu(db)
#         print("Closing")
# =============================================================================
                
        
    
###############################################################################



    
 
###############################################################################
    
        
    
        
            
 
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
    print("1. Print Session type \n2. Print Exercise \n")
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
    
    else:
        print("Closing.")
    
###############################################################################

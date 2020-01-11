from utils import helper as he
from parsing import converter as conv
import connect as con
import request as re
from cache import cache
from backup import backup
from crud import insert
from menu import submenu
from menu import utils as menu_utils
from utils import filter
from analyze import analyse_strength, analyse_run, analyse_off


def user_start(client):
    if not cache.is_empty() and client != None:
        print(he.indent())
        decision = input("Cache can be uploaded. Confirm [y/n]: ")
        if decision == "y":
            cache.upload_cache()
    print(he.indent())
    
    print("1. Session \n2. Cache \n3. Backup")
    decision = input("\nChoose number or press enter for exit: ")
    #options = ["strength", "run", "off", "hike"]
    try:
        decision = int(decision)
    except: 
        print("Closing")
        quit()
    
    if decision == 1:
        client = con.connect_to_client()
        db = client["TrainingLogData"]
        session_menu(db)
        client.close()      
    elif decision == 2:
        menu_cache()
    elif decision == 3:
        backup_menu()           
    else:
        print("Exit.")


def session_menu(db):
    print("1. Create \n2. Read \n3. Update \n4. Delete")
    
    decision = input("\nChoose number or press enter for exit: ")
    
    print(he.indent())
    
    if decision == "1":
        insert.insert_session(db)
    
    elif decision == "2":
        submenu.read(db, submenu.read_decision())

    elif decision == "3":
        date = input("Date to change (dd.mm.yy): ")
        cons_day = he.get_day_in_year(date)
        sessions = re.find_session(db["AllSessions"], cons_day)
        session = menu_utils.get_session_from_user(sessions=sessions)
        submenu.edit(session, db["AllSessions"])
        
    elif decision == "4":
        date = input("Date to delete (dd.mm.yy): ")
        cons_day = he.get_day_in_year(date)
        sessions = re.find_session(db["AllSessions"], cons_day)
        session = menu_utils.get_session_from_user(sessions=session)
        dec = input("Delete this session [y/n]: ")
        if dec == "y": re.delete_session(db["AllSessions"], cons_day)
    else:
        print("Closing")
              
    
def menu_cache():
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
        

def backup_menu():
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
                
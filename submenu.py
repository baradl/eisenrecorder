import user_interaction as ui
import helper as he
import menu
import request as re
import converter as conv
import printer
from datetime import datetime
import filter


###############################################################################

"""
If a session shall be edited the user is guided via this menu. 
"""

def edit(session, col):
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
        if session["type"] != "run":
            while True:
                new_ex = input("New exercise: ")
                if len(new_ex) < 4: break
                new_ex = conv.convert_input(new_ex)
                re.updater.update_exercise(session, new_ex, col)
            
        else:
            new_ex = input("New Run: ")
            new_ex = conv.convert_run(new_ex)
            re.updater.update_exercise(session, new_ex, col)  
    elif dec == "4":
        ex = input("List exercises to be deleted: ")
        ex_list = ex.split()
        re.updater.delete_exercise(session, ex_list, col)
        
    elif dec == "5":
        newcomment = input("New comment: ")
        re.updater.update_comments(session, newcomment, col)
        
    else:
        dec = input("No valid input. Back to menu [y/n]: ")
        if dec == "y": edit()
        else: raise SystemExit
    
    re.printer.print_session(session)
    dec = input("Back to main menu [y/n]: ")
    if dec == "y": menu.user_start(col.database)


###############################################################################
    
    
    """
Menu to let the user input the sessions one wants to print.
""" 
    
def read(db, decision, type_):
    if decision == "single":
        date = input("Date of session (dd.mm.yy): ")
        cons_day = he.get_day_in_year(date)
        
        col = db["AllSessions"]
        session = re.find_session(col, cons_day)
        re.printer.print_session(session)
    elif decision == "week":
        dec = input("Current week[y/n]: ")
        if dec == "y": 
            day = str(datetime.now().day)
            month = str(he.month_now())
            year = str(he.year_now())
            
            date = day + "." + month + "." + year
        else:
            date = input("Date in week of interest: ")
        
        [start, end] = he.get_week(date)
        
        
        doc_list = filter.filter_consecutive_days(db, start, end, type_)
        
        printer.print_filter(doc_list)
    
    elif decision == "month":
        date = input("mm.yyyy: ")
        [month, year] = date.split(".")
        
        if len(year) == 2: year = "20" + year
        
        month = conv.convert_month_to_int(month)
        
        monthly_days = he.monthly_days(int(year))
        
        days = [sum(monthly_days[:month-1])+1,sum(monthly_days[:month])]
        
        sessions = filter.filter_consecutive_days(db,days[0], days[1], type_)
        printer.print_filter(sessions)
    
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

        
def cud_actions():
    print("1. Insert \n2. Change \n3. Delete")
    decision = input("\nChoose number or press enter for exit: ")
    
    return decision

def insert(db, type_):
    if type_ == "strength":
        print("'name sets reps weight' or 'name reps weight'")
        see_abb = input("See abbreviation [y/n]: ")
        if see_abb == "y": he.abbreviation()
        ui.insert_strength(db)
    elif type_ == "run":
        ui.insert_run(db)
    elif type_ == "off":
        ui.insert_off(db)
    
def read_decision():
    choices = ["Session", "Week", "Month", "Year", "All"]
    print("1. Session \n2. Week \n3. Month \n4. Year \n5. All")#
    dec = input("\nChoose number or press enter for exit: ")
    try:
        dec = int(dec)
        return choices[dec - 1].lower()
    except:
        return None
        
        

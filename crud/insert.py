import request as re
from utils import helper as he
from parsing import converter as conv
from utils import check
from crud import utils as crud_utils
from crud import printer

from menu import menu
from cache import cache

import sys


def insert_session(db):
    col = db["AllSessions"]
    print(he.indent())    
    date = crud_utils.get_date_from_user()

    cons_day = he.get_day_in_year(date)          
    workout_type = input("workout type: ")

    if workout_type == "off":
        pass
    elif workout_type == "run":
        content = crud_utils.construct_run()
    elif workout_type in he.STRENGHT_TYPES:
        content = crud_utils.construct_exercises()
    elif workout_type == "hike":
        content = crud_utils.construct_hike()
    elif workout_type == "cardio":
        content = crud_utils.construct_cardio()
    else:
        print("No valid session type. Exit.")
        sys.exit()
    
        
    comment_ = input("Any comments regarding the session: ")
    if len(comment_) < 3: comment_ = ""
        
    dic = re.construct_dict_session(cons_day, workout_type, content, comment_)
    
    print(he.indent())  
    print("Insert following session:")
    printer.print_session(dic)
    print(he.indent())

    decision = input("Correct [y/n]: ")
    if decision == "y": re.insert_session(col, dic)
    else: insert_session(db)
    
    decision = input("Insert another session [y/n]: ")
    if decision == "y": insert_session(db)   
    
import pickle
from utils import helper as he
from utils import check
import os, glob
from request import delete_session

BACKUP_DIR = "../../backup/"

def create_backup(col):
    if type(col) is str:assert col == "AllSessions"
    else: assert col.name == "AllSessions"
    cursor = col.find()
    global BACKUP_DIR
    for document in cursor:
        name = str(document["day"])
        if len(name) == 1: name = "0" + name
        filepath = BACKUP_DIR + name + ".txt"
        pickle.dump(document, open(filepath, "wb"))
        

def check_backup():
    days = he.get_days_dir()
    multi = False
    missing = False
    mist = check.check_int_list(days)
    if mist[0] != []:
        multi = True
        print("These days were more than once mentioned:", mist[0])
    if mist[1] != []:
        missing = True
        print("These days were not mentioned:", mist[0])
        
    if not missing and not multi:
        print("All sessions ("+ str(max(days)) +") in backup")
        
        
def upload_backup(db):
    global BACKUP_DIR
    os.chdir(BACKUP_DIR)
    col_name = "AllSessions_backup"
    col_name_new = col_name
    k = 1
    while col_name_new in db.list_collection_names():
        col_name_new = col_name + str(k)
        k += 1
        
     
    col = db[col_name_new]
    
    for file in glob.glob("*.txt"):
        document = pickle.load(open(file, "rb"))
        col.insert_one(document)
        
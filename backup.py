"""
Collection of back_up functions
"""







import pickle
import helper as he
from helper import check
import os, glob
#from request import delete_session



"""
Creates local backup for given collection. In this case the collection of interest
is "AllSessions". Files are saved on machine as pickled files. File name is the 
consecutive number of days (beginning at 01.01.2019) corresponding to its date.
"""
def create_backup(col):
    if type(col) is str:assert col is "AllSessions"
    else: assert col.name is "AllSessions"
    cursor = col.find()
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/backup/"
    for document in cursor:
        name = str(document["day"])
        if len(name) == 1: name = "0" + name
        filepath = directory + name + ".txt"
        pickle.dump(document, open(filepath, "wb"))
        



"""
Checks the backup for multiple or missing entries. Informs user about respective
dates (either missing or multiple times mentioned).
Mist is a list of two lists. These two lists contain the missing days and the 
multiple mentioned days.
If no mistakes have been made the user is informed about the number of backed up
sessions.
"""
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
        
        


"""
The local backup can be uploaded. It is verified that no uploaded backup already
exists. If that is the case the name of the new upload is changed.
To upload files the backup is unpickled.
"""

def upload_backup(db):
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/backup/"
    os.chdir(directory)
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
        

        
    
    
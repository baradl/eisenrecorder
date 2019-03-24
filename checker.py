"""
Collection of checking functions that interact with the database.
"""
TYPES = ["off", "run", "SQ", "DL", "BP", "UB", "LB"]


###############################################################################
"""
Check existence of Database
"""

def check_db_exist(db, myclient):
    dblist = myclient.list_database_names()
    if db.name in dblist:
        #print("The database exists.")
        return True
    else: 
        #print("The database does not exist.")
        return False

###############################################################################
"""
Check existence of Collection
"""
        

def check_col_exist(db, col):
    collist = db.list_collection_names()
    if col.name in collist:
        #print("The collection exists.")
        return True
    else: 
        #print("The collection does not exist.")
        False

###############################################################################
"""
Check existence of Document by Day
"""
def check_doc_exist(db, col, day):
    for document in col.find():
        if document["day"] == day:
            return True
    return False


###############################################################################
    
"""
Check existence of Document by ID
"""
def alreadyExists(ID,col):
    if type(col.find_one({'_id': ID})) == dict:
        return True
    else:
        return False

###############################################################################

"""
Sets the exercise list according to exercises in the session.
"""
def check_exlist(doc):
    ex_list = []
    typ = doc["type"]
    assert typ in TYPES and typ != "run" and typ != "off"
    check_amount(doc)
    for i in range(doc["amount of exercises"]):
        ex = doc["exercise" + str(i+1)]
        ex_list.append(ex[0])
    doc["exercise list"] = ex_list

###############################################################################
    
"""
Sets the amount of exercises according to exercises in session (not according to
the exercise list)
"""
def check_amount(doc):
    global TYPES
    keys = doc.keys()
    typ  = doc["type"]
    if typ in TYPES and typ != "off" and typ != "run":
        doc["amount of exercises"] = len(keys) - 5
























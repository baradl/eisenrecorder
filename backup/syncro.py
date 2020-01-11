import request as re
from utils import helper


def merge_backups(col1,col2):
    db = col1.database
    name1 = col1.name
    name2 = col2.name
    
    assert name1 != name2
    if name1 == "AllSessions": 
        pass
    elif name2 == "AllSessions":
        [col1, col2] = helper.swap(col1,col2)
    else:
        assert "AllSessions_backup" in name1 and "AllSessions_backup" in name2
        
        
        number1 = col1.name.replace("AllSessions_backup","")
        number2 = col2.name.replace("AllSessions_backup","")
        
        if number1 == "":
            pass
        elif number2 == "":
            [col1, col2] = helper.swap(col1,col2)
        elif int(number1) > int(number2):
            [col1, col2] = helper.swap(col1,col2)
        
    for document in col1.find():
        if re.checker.check_doc_exist(db, col2, document["day"]): continue
        else: col2.insert_one(document)
    for document in col2.find():
        #print(document)
        if re.checker.check_doc_exist(db, col1, document["day"]): continue
        else: col1.insert_one(document)
    
    db.drop_collection(col2)
    


def merge_all(db):
    dblist = db.list_collection_names()
    backups = helper.find_substring_in_stringlist(dblist, "AllSessions_backup")
    
    if backups == []:
        print("No backup in Database. Exit.")
    else:
        backups.sort(reverse = True)
        for i in range(len(backups)-1):
            merge_backups(db[backups[i+1]], db[backups[i]])
        merge_backups(db["AllSessions"], db["AllSessions_backup"])   
            
            
            
# =============================================================================
#             
# ###############################################################################
#             
# def sync_clients(direction):
#     """
#     Direction "up" indicates that online database shall be updated according to
#     changes in offline db and vice versa for "off".
#     
#     local = True indicates that client_rec is the client for offline dbs and vice
#     versa for local = False
#     """
#     assert direction == "up" or "down"
#     if direction == "down": local = True
#     else: local = False
#     
#     client_old = con.connect_to_client(local)
#     client_new = con.connect_to_client(not local)
#     
#     db_list_new = client_new.list_database_names()
#     if direction == "down":
#         db_list_new.remove("admin")
#         db_list_new.remove("local")
#     else:
#         db_list_new.remove("admin")
#         db_list_new.remove("local")
#         db_list_new.remove("config")
#     #db_list_new.remove("config")
#     for db_name_new in db_list_new:
#         #print(db_name_new)
#         db_new = client_new[db_name_new]
#         db_old = client_old[db_name_new]
#         col_list_new = db_new.list_collection_names()
#         for col_name_new in col_list_new:
#             #print(col_name_new)
#             col_new = db_new[col_name_new]
#             col_old = db_old[col_name_new]
#             cursor_new = col_new.find()
#             for document in cursor_new:
#                 #print(document)
#                 if re.checker.check_doc_exist(db_old, col_old, document["day"]): continue
#                 else: col_old.insert_one(document)
#     
#     db_list_old= client_old.list_database_names()
#     if direction == "down":
#         db_list_old.remove("admin")
#         db_list_old.remove("local")
#         db_list_old.remove("config")
#     else:
#         db_list_old.remove("admin")
#         db_list_old.remove("local")
#         
#     for db_name_old in db_list_old:
#         #print(db_name_old)
#         db_old = client_old[db_name_old]
#         db_new = client_new[db_name_old]
#         col_list_old = db_old.list_collection_names()
#         for col_name_old in col_list_old:
#             #print(col_name_old)
#             col_old = db_old[col_name_old]
#             col_new = db_new[col_name_old]
#             cursor_old = col_old.find()
#             for document in cursor_old:
#                 #print(document)
#                 if re.checker.check_doc_exist(db_new, col_new, document["day"]): continue
#                 else: col_old.delete_one(document)
# 
# 
# 
# 
# ###############################################################################
#     
# 
# 
# 
# def sync_dbs(direction, db_name):
#     assert direction == "up" or "down"
#     if direction == "down": local = True
#     else: local = False
#     
#     client_old = con.connect_to_client(local)
#     client_new = con.connect_to_client(not local)
#     
#     db_new = client_new[db_name]
#     db_old = client_old[db_name]
#     
#     assert re.checker.check_db_exist(db_new,client_new)
#     col_list_new = db_new.list_collection_names()
#     for col_name_new in col_list_new:
#             #print(col_name_new)
#             col_new = db_new[col_name_new]
#             col_old = db_old[col_name_new]
#             cursor_new = col_new.find()
#             for document in cursor_new:
#                 #print(document)
#                 if re.checker.check_doc_exist(db_old, col_old, document["day"]): continue
#                 else: col_old.insert_one(document)
#     col_list_old = db_old.list_collection_names()
#     for col_name_old in col_list_old:
#         #print(col_name_old)
#         col_old = db_old[col_name_old]
#         col_new = db_new[col_name_old]
#         cursor_old = col_old.find()
#         for document in cursor_old:
#             #print(document)
#             if re.checker.check_doc_exist(db_new, col_new, document["day"]): continue
#             else: col_old.delete_one(document)
#             
#  
# 
# 
# ###############################################################################
#     
# 
# =============================================================================
           

        

    












    

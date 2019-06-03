import pymongo as pm
import requests


###############################################################################

"""
Connects to MongoDB Client. Local Option not used anymore.
"""


def connect_to_client(local = False):
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/"
    if not local:        
        with open(directory + "login_data.txt", "r") as login:
            mongodb_url = login.readlines()
    
        client = pm.MongoClient(mongodb_url)
    else: client = pm.MongoClient()
    return client



###############################################################################

"""
Checks current connection. Returns boolean value according to status.
"""

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
   


###############################################################################

# =============================================================================
# """
# Checks if given host is local host.
# """
#     
# def is_host_local(client):
#     if client == pm.mongo_client.MongoClient(host=['localhost:27017'], 
#                                               document_class=dict, 
#                                               tz_aware=False, connect=True):
#         return True
#     else: return False
# =============================================================================



###############################################################################    
    
# =============================================================================
# """
# Menu to let the user choose type of connection (online/offline).
# """    
#        
# def user_connect_to_client():
#     dec2 = input("Connect to offline (off) or online (on) client?\n")        
#     if dec2 == "on":
#         myclient = connect_to_client()
#         print("Connected to MongoDB-Cluster by Brad.")
#         print(he.indent())
#     elif dec2 == "off":
#         myclient = connect_to_client(local = True)
#         print("Connected to local Client.")
#         print(he.indent())
#     else: 
#         print("No valid input. Shutting down.")
#         raise SystemExit
#     return myclient
# =============================================================================
    
    
    
    
    
    
    
    
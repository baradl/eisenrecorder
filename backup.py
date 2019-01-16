import pickle,os 

def create_backup(col):
    if type(col) is str:assert col is "AllSessions"
    else: assert col.name is "AllSessions"
    cursor = col.find()
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/backup/"
    for document in cursor:
        name = document["day"]
        filepath = directory + name + ".txt"
        pickle.dump(document, open(filepath, "wb"))#
        



def print_backup():
    directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/backup/"
    os.chdir(directory)
    files = glob.glob("*.txt")
        
        
        
    
    
import connect
import request



def create(db, col = "empty"):
    client = connect.connect_to_client()
    db = client[db]
    if col != "empty":
        col = db [col]
        return db,col
    return db
    
    


def find(col, day):
    return request.find_session(col,day)



    
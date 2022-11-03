import sqlite3 
import time
import sys
import random
import datetime


def session_start():
    global connection, cursor, session_id, uid
    #the session_start() function checks for a session id to see if a session is already in place or not
    #the system assigns a session number incase its not started.
    if session_id != None:
        print("End the current session before starting a new session")
    else:
        while True:
            session_id = (random.randint(1,10000))
            cursor.execute("SELECT COUNT(sno) FROM sessions WHERE uid = ? and sno = ?;",(uid,session_id))
            sessionoccurences = cursor.fetchone()
            startDate = datetime.now(0).strftime("%d %m %Y %h: %m")
            endDate = None
            if sessionoccurences > 0:
                session_id = None
                print("The system assigned you a session number which has already been used")
            else:
                cursor.execute("INSERT INTO sessions(uid,sno,start,end) VALUES (?,?,?,?);",(uid,session_id,startDate,endDate))
                connection.commit()
                break



def end_session():
    global connection, cursor, session_id, uid

    if session_id != None:
        endDate = datetime.now(0).strftime("%d %m %Y %h: %m")
        cursor.execute('UPDATE sessions(uid,sno,start,end) SET end = ? WHERE uid=? AND session_id =?;',(endDate,uid,session_id))
        connection.commit()
        session_id = None
    else:
        print("You are trying to end a session which is not being utilized")
		
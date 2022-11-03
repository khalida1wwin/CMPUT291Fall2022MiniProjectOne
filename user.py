import sqlite3 
import time
import sys
import random
import datetime


def session_start(connection,cursor,session_id,uid):
    #the session_start() function checks for a session id to see if a session is already in place or not
    #the system assigns a session number incase its not started.
    if session_id != None:
        print("End the current session before starting a new session")
    else:
        while True:
            session_id = (random.randint(1,10000)) #assigning a random session id with a value b/w 1 and 10000
            cursor.execute("SELECT COUNT(sno) FROM sessions WHERE uid = ? and sno = ?;",(uid,session_id))
            sessionoccurences = cursor.fetchone()
            startDate = datetime.now(0).strftime("%d %m %Y %h: %m")
            endDate = None
            if sessionoccurences == 0: # checks if a session id has been repeated for a particular user
                cursor.execute("INSERT INTO sessions(uid,sno,start,end) VALUES (?,?,?,?);",(uid,session_id,startDate,endDate))
                #updates the sessions table with recorded data
                connection.commit()
                break
            else:
                session_id = None
                print("The system assigned you a session number which has already been used")
                
    return session_id,uid




def end_session(connection,cursor,session_id,uid):
    # checks for a valid and an active session id to 
    if session_id != None:
        endDate = datetime.now(0).strftime("%d %m %Y %h: %m")
        cursor.execute('UPDATE sessions(uid,sno,start,end) SET end = ? WHERE uid=? AND session_id =?;',(endDate,uid,session_id))
        connection.commit()
        session_id = None
    else:
        print("You are trying to end a session which is not being utilized")
    
    return session_id,uid
		
def searchSongs(connection,cursor,session_id,uid):
    
    #takes the user keyword or a bunch of user keywords.
    userkeywords = input("please enter your keywords to find matching songs: ").split()
    if len(userkeywords) == 0:
        print("please enter a valid keyword/ keywords.")
        return
    # the entire song query is broken into chunks of the overall query.
    # The songquery variable aims to display at the most top 5 matches in response 
    # to keyword entry 
    songquery = "SELECT DISTINCT s.sid, s.title, s.duration FROM songs s"
    index = 0
    for word in userkeywords:
	    if index == 0:
	        songquery += " AND (s.title LIKE '%{}%' )".format(word)
        else:
	        songquery += " OR (s.title LIKE '%{}%' )".format(word)
        index += 1
    songquery += " ORDER BY ("
    for word in userkeywords:
        songquery += "CASE WHEN s.title LIKE '%{}%' THEN 1 ELSE 0 END + ".format(word)
    songquery.rstrip("+ ")
    songquery += ") DESC;"

    if sqlite3.complete_statement(songquery):
        cursor.execute(songquery)
        matchingsongs = cursor.fetchall()

        if len(matchingsongs) == 0:
            print("No matching songs found!")
            return
        elif len(matchingsongs) <= 5:
            for i in range(len(matchingsongs)):
                print("Song ",i+1,matchingsongs[i])
                while True:
                    useroption = input("Select a song or press enter ")
                    if useroption.isnumeric():
                        break
                    song_id = matchingsongs[useroption -1][0]
                    action = input("Please enter a song action to perform: 1 action a 2 actiob b...")
                    if action.upper() == 1:
                        addSong(song_id)
                    # if action == 2:
                        #
        else:
            for i in range(len(matchingsongs)):
                if i > 5:
                    while True:
                        userpotion = input('Select a song or press enter to see more matches:  ')
                        if  len(useroption) == 0 or userpotion.isnumeric():
                            break
                    if len(useroption) == 0:
                        for k in range(5, len(matchingsongs)):
                            print("Song ",k+1, matchingsongs[k])
                        while True:
							useroption2 = input("Please Select a song: ")
							if useroption2.isnumeric():
								break
						song_id = matchingsongs[useroption2-1][0]
                        action = input("Would you like to access the songAction() menu? Press Y")
                        if action.upper() == 'Y':
                            songAction(song_id,uid)
					    break
					else:
						song_id = matchingsongs[useroption-1][0]
                        action = input("Would you like to access the songAction() menu? Press Y")
                        if action == 'Y':
                            songAction(song_id,uid)
					    break
				print(i+1, matchingsongs[i])
    else:
		print("The query failed to fetch data")



def searchPlaylists(connection,cursor,session_id,uid):
    
    #takes the user keyword or a bunch of user keywords.
    userkeywords = input("please enter your keywords to find matching playlists: ").split()
    if len(userkeywords) == 0:
        print("please enter a valid keyword/ keywords.")
        return

    songquery = "SELECT DISTINCT p.pid, s.title, s.duration FROM songs s"
    index = 0
    for word in userkeywords:
        if index == 0:
            songquery += " AND (s.title LIKE '%{}%' )".format(word)
        else:
            songquery += " OR (s.title LIKE '%{}%' )".format(word)
        index += 1
    songquery += " ORDER BY ("
    for word in userkeywords:
        songquery += "CASE WHEN s.title LIKE '%{}%' THEN 1 ELSE 0 END + ".format(word)
    songquery.rstrip("+ ")
    songquery += ") DESC;"

    if sqlite3.complete_statement(songquery):
        cursor.execute(songquery)
        matchingsongs = cursor.fetchall()

        if len(matchingsongs) == 0:
            print("No matching songs found!")
            return
        elif len(matchingsongs) <= 5:
            for i in range(len(matchingsongs)):
                print("Song ",i+1,matchingsongs[i])
                while True:
                    useroption = input("Select a song or press enter ")
                    if useroption.isnumeric():
                        break
                    song_id = matchingsongs[useroption -1][0]
                    action = input("Please enter a song action to perform: 1 action a 2 actiob b...")
                    if action == 1:
                        addSong(song_id)
                    # if action == 2:
                        #
        else:
            for i in range(len(matchingsongs)):
                if i > 5:
                    while True:
                        userpotion = input('Select a song or press enter to see more matches:  ')
                        if  len(useroption) == 0 or userpotion.isnumeric():
                            break
                    if len(useroption) == 0:
                        for k in range(5, len(matchingsongs)):
                            print("Song ",k+1, matchingsongs[k])
                        while True:
                            useroption2 = input("Please Select a song: ")
                            if useroption2.isnumeric():
                                break
						# song_id = matchingsongs[useroption2-1][0]
                        action = input("Would you like to access the songAction() menu? Press Y")
                        if action == 'Y':
                            songAction(song_id,uid)
                        # if action ==
					    break
					else:
						song_id = matchingsongs[useroption-1][0]
                        action = input("Would you like to access the songAction() menu? Press Y")
                        if action == 'Y':
                            songAction(song_id,uid)
					    break
				print(i+1, matchingsongs[i])
    else:
		print("The query failed to fetch data")




    


		



                


        
        





    
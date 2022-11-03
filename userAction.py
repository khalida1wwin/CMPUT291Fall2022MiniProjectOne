
import random
import datetime
import main
import songactions

def session_start(session_id,uid,connection,cursor):
    #the session_start() function checks for a session id to see if a session is already in place or not
    #the system assigns a session number incase its not started.
    if session_id != None:
        print("End the current session before starting a new session")
    else:
        while True:
            session_id = (random.randint(1,10000)) #assigning a random session id with a value b/w 1 and 10000
            sessionoccurences = cursor.execute("SELECT COUNT(sno) FROM sessions WHERE uid = ? and sno = ?;",(uid,session_id))
            sessionoccurences = cursor.fetchone()
            startDate = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
            endDate = None
            if sessionoccurences[0] == 0: # checks if a session id has been repeated for a particular user
                cursor.execute("INSERT INTO sessions(uid,sno,start,end) VALUES (?,?,?,?);",(uid,session_id,startDate,endDate))
                #updates the sessions table with recorded data
                connection.commit()
                return session_id,startDate

                
            else:
                session_id = None
                
    return session_id,startDate




def end_session(session_id,uid,connection,cursor):
    # checks for a valid and an active session id to successfully end an ongoing session,
    # and update the relevant data associated with a session of a user.
    if session_id != None:
        endDate = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
        cursor.execute('UPDATE sessions SET end = ? WHERE uid=? AND sno =?;',(endDate,uid,session_id))
        connection.commit()
        print("Session ended successfully!")
        session_id = None
        return session_id
    else:
        print("You are trying to end a session which is not being utilized")
    
    return session_id
		
def searchSongs(session_id,uid,connection,cursor):
    
    #takes the user keyword or a bunch of user keywords.
    userkeywords = input("please enter your keywords to find matching songs: ").split()
    if len(userkeywords) == 0:
        print("please enter a valid keyword/ keywords.")
        return
    # the entire song query is broken into chunks of the overall query.
    # The songquery variable aims to display at the most top 5 matches in response 
    # to keyword entry 
    songquery = "SELECT DISTINCT s.sid, s.title, s.duration FROM songs s"
    # print(userkeywords)
    # print("songquery",songquery)
    index = 0
    for word in userkeywords:
            # print(songquery)
            if index == 0:
                songquery += " WHERE (s.title LIKE '{}' )".format(word)
            else:
                songquery += " OR (s.title LIKE '{}' )".format(word)
            index += 1
    songquery += " ORDER BY ("
    for word in userkeywords:
        songquery += "CASE WHEN s.title LIKE '{}' THEN 1 ELSE 0 END + ".format(word)
    songquery = songquery.rstrip("+ ")
    songquery += ") DESC;"

    # print(songquery)
    cursor.execute(songquery)
    matchingsongs = cursor.fetchall()

    if len(matchingsongs) == 0:
        print("No matching songs found!")
        return
    elif len(matchingsongs) <= 5:
        for i in range(len(matchingsongs)):
            print("Song ",i+1,matchingsongs[i])
        while True:
            useroption = input("Select a song(Numerical Value) to view details or press enter to exit")
            if useroption.isnumeric():
                # break
                song_id = matchingsongs[int(useroption) -1][0]
                # action = input("Please enter a song action to perform: 1 action a 2 actiob b...")
                songactions.songAction(song_id, uid,connection, cursor)
                break
            elif len(useroption) == 0:
                #TODO go to main command.
                break
            
               
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
                    song_id = matchingsongs[int(useroption2)-1][0]
                    action = input("Would you like to access the songAction() menu? Press Y")
                    if action.upper() == 'Y':
                        songactions.songAction(song_id,uid,connection,cursor)
                    break
                else:
                    song_id = matchingsongs[int(useroption)-1][0]
                    action = input("Would you like to access the songAction() menu? Press Y")
                    if action.upper() == 'Y':
                        songactions.songAction(song_id,uid,connection,cursor)
                    break
            print(i+1, matchingsongs[i])
    





    
def searchPlaylists(session_id,uid,connection,cursor):
    
    #takes the user keyword or a bunch of user keywords.
    userkeywords = input("please enter your keywords to find matching playlists: ").split()
    if len(userkeywords) == 0:
        print("please enter a valid keyword/ keywords.")
        return
    # the entire playlist query is broken into chunks of the overall query.
    # The playlistquery variable aims to display at the most top 5 matches in response 
    # to keyword entry 
    playlistquery = "SELECT DISTINCT p.pid, p.title, s.duration FROM songs s, playlists p, plinclude pl WHERE p.pid = pl.pid AND pl.sid = s.sid"
    index = 0
    for word in userkeywords:
            
            if index == 0:
                playlistquery += " AND (p.title LIKE '{}' )".format(word)
            else:
                playlistquery += " OR (p.title LIKE '{}' )".format(word)
            index += 1
    playlistquery += " ORDER BY ("
    for word in userkeywords:
        playlistquery += "CASE WHEN p.title LIKE '{}' THEN 1 ELSE 0 END + ".format(word)
    playlistquery = playlistquery.rstrip("+ ")
    playlistquery += ") DESC;"

    # the following lines of code execute the SQL search on the data base provided
    cursor.execute(playlistquery)
    matchingplaylists = cursor.fetchall()
    # using a case basis approach to evaluate our problem and provide the user with necessary options.
    if len(matchingplaylists) == 0:
        print("No matching playlists found!")
        return
    elif len(matchingplaylists) <= 5:
        for i in range(len(matchingplaylists)):
            print("Playlist ",i+1,matchingplaylists[i])
        while True:
            useroption = input("Select a Playist(Numeric input) or press enter ")
            if useroption.isnumeric():
                    
                playlist_id = matchingplaylists[int(useroption) -1][0]
                playlistsDesc(playlist_id,uid,connection,cursor)
                break
            else:
                #TODO go to main menu?
                break
               
    else:
        #the following lines of code is executed when more than 5 entries to a query search is detected.
        for i in range(len(matchingplaylists)):
            if i > 5:
                while True:
                    userpotion = input('Select a Playist(Numeric input) or press enter to see more matches:  ')
                    if  len(useroption) == 0 or userpotion.isnumeric():
                        break
                if len(useroption) == 0:
                    for k in range(5, len(matchingplaylists)):
                        print("Playlist ",k+1, matchingplaylists[k])
                    while True:
                            useroption2 = input("Please Select a Playlist(Numeric Value) or press enter to view more: ")
                            if useroption2.isnumeric():
                                break
                    playlist_id = matchingplaylists[int(useroption2)-1][0]
                    action = input("Would you like to access the playlistDescription() menu? Press Y")
                    if action.upper() == 'Y':
                        playlistsDesc(playlist_id,uid,connection,cursor)
                    break


                else:
                    playlist_id = matchingplaylists[int(useroption)-1][0]
                    action = input("Would you like to access the playlistDescription() menu? Press Y")
                    if action.upper() == 'Y':
                        playlistsDesc(playlist_id,uid,connection,cursor)
                    break
            print(i+1, matchingplaylists[i])


def playlistsDesc(playlist_id,uid,connection,cursor):
    #the playlist description function is called when the user chooses to view the list of songs 
    # from a playlist 
    playlistsongquery = "SELECT s.sid, s.title, s.duration FROM songs s, playlists p, plinclude pl WHERE p.pid = {0} AND p.uid = {1} AND p.pid = pl.pid AND pl.sid = s.sid; ".format(playlist_id,uid)
    cursor.execute(playlistsongquery)
    plsongs = cursor.fetchall()
    print("The Songs of your Playlist are: ")
    if len(plsongs)!=0:
        for i in range(len(plsongs)):
            print(i+1,plsongs[i])
        while True:
            #Allowing the user to interact with their chosen song and perform their actions.
            userinput = input("Would you like to view a song(Numeric Input) and its details or exit?")
            if (userinput.isnumeric()) and (userinput <= len(plsongs)):
                song_id = plsongs[int(userinput) - 1][0]
                songactions.songAction(song_id,uid,connection,cursor)
                break
            else:
                print("Please enter a valid input!")
    else:
        print("Oops! Your Playlist is empty :(")


def searchArtists(session_id,uid,connection,cursor):
    
    #takes the user keyword or a bunch of user keywords.
    userkeywords = input("please enter your keywords to find matching playlists: ").split()
    if len(userkeywords) == 0:
        print("please enter a valid keyword/ keywords.")
        return
    # the entire playlist query is broken into chunks of the overall query.
    # The playlistquery variable aims to display at the most top 5 matches in response at a time if matches exceed more than 5 entries
    # to keyword entry 
    artistquery = "SELECT DISTINCT a.name, a.nationality, COUNT(p.sid) FROM artists a, perform p, songs s WHERE p.aid = a.aid AND p.sid = s.sid "
    index = 0
    for word in userkeywords:
            
            if index == 0:
                artistquery += " AND (a.name LIKE '{}' OR s.title LIKE '{}' )".format(word,word)
            else:
                artistquery += " OR (a.name LIKE '{}'OR s.title LIKE '{}' )".format(word,word)
            index += 1
    artistquery += " ORDER BY ("
    for word in userkeywords:
        artistquery += "CASE WHEN a.name LIKE '{}' THEN 1 ELSE 0 END + CASE WHEN s.title LIKE '{}' THEN 1 ELSE 0 END + ".format(word,word)
    artistquery = artistquery.rstrip("+ ")
    artistquery += ") DESC;"

    # executing the query to find relevant matches
    cursor.execute(artistquery)
    matchingartists = cursor.fetchall()

    if len(matchingartists) == 0:
        print("No matching playlists found!")
        return
    elif len(matchingartists) <= 5:
        print("ArtistName","Nationality","#songs performed")
        for i in range(len(matchingartists)):
            print(i+1,matchingartists[i])
        while True:
            useroption = input("Select a Artist(Numeric input) or press enter ")
            if useroption.isnumeric():
                    
                artist_id = matchingartists[int(useroption) -1][0]
                artistsDesc(artist_id,uid,connection,cursor)
                break
            else:
                #TODO go to main menu?
                break
               
    else:
        for i in range(len(matchingartists)):
            if i > 5:
                while True:
                    userpotion = input('Select an Artist(Numeric input) or press enter to see more matches:  ')
                    if  len(useroption) == 0 or userpotion.isnumeric():
                        break
                if len(useroption) == 0:
                    print("ArtistName","Nationality","#songs performed")
                    for k in range(5, len(matchingartists)):
                        print(k+1, matchingartists[k])
                    while True:
                            useroption2 = input("Please Select an artistt: ")
                            if useroption2.isnumeric():
                                break
                    # song_id = matchingsongs[useroption2-1][0]
                    artist_id = matchingartists[int(useroption2)-1][0]
                    action = input("Would you like to access the artistDescription() menu? Press Y")
                    if action.upper() == 'Y':
                        artistsDesc(artist_id,uid,connection,cursor)
                    break


                else:
                    artist_id = matchingartists[int(useroption)-1][0]
                    action = input("Would you like to access the playlistDescription() menu? Press Y")
                    if action.upper() == 'Y':
                        artistsDesc(artist_id,uid,connection,cursor)
                    break
            print(i+1, matchingartists[i])


def artistsDesc(artist_id,uid,connection,cursor):
    artistsongquery = "SELECT s.sid, s.title, s.duration FROM songs s, artists a, perform p WHERE a.aid = {} AND p.aid = a.aid AND p.sid = s.sid; ".format(artist_id)
    cursor.execute(artistsongquery)
    artsongs = cursor.fetchall()
    print("The Songs of your Artist are: ")
    if len(artsongs)!=0:
        for i in range(len(artsongs)):
            print(i+1,artsongs[i])
        while True:
            userinput = input("Would you like to view a song(Numeric Input) and its details or exit?")
            if (userinput.isnumeric()) and (userinput <= len(artsongs)):
                song_id = artsongs[int(userinput) - 1][0]
                songactions.songAction(song_id,uid,connection,cursor)
                break
            else:
                print("Please enter a valid input!")
    else:
        print("Oops! Your Artist's performance list is empty :(")





		



                


        
        






import sqlite3
import string
import main
import userAction
session_id = None
def info(sid,uid,connection, cursor):
    # More information for a song is the names of artists who performed it 
    # in addition to id, title and duration of the song as well as the names of 
    # playlists the song is in (if any).
    print("Song Details:")
    cursor.execute('''SELECT sid, title, duration 
                    FROM songs 
                    WHERE sid =:SID''', {"SID":sid})
    all_entry = cursor.fetchall()
    for one_entry in all_entry:
        print(one_entry)
    print("\nArtist Details:")
    cursor.execute('''SELECT a.name
                    FROM perform p, artists a
                    WHERE p.sid =:SID
                    AND a.aid = p.aid''', {"SID":sid})
    artists = cursor.fetchall()
    for one_entry in artists:
        print(one_entry)
    print("\nPlaylist Details:")
    cursor.execute('''SELECT p.title 
                    FROM playlists p, plinclude pl
                    WHERE pl.pid = p.pid 
                    AND pl.sid =:SID''', {"SID":sid})
    playlist = cursor.fetchall()
    for one_entry in playlist:
        print(one_entry)
    songAction(sid,uid,connection, cursor) # Go back to the menu after everything is done??
    return

def listen(sid, uid,connection, cursor):
    #This function updates the listen count if a song is already listened to in a session. It inserts
    # a listen event to the session if the song is not listened to in the session. It creates a new session, if there is no existing one.
    checkSession = '''SELECT sno FROM sessions
                    WHERE uid=:UID 
                    AND end IS NULL;'''
    cursor.execute(checkSession, {"UID":uid})
    sessionExist = cursor.fetchall()
    # print(sessionExist)
    if len(sessionExist) == 0:
        sno,Date = userAction.session_start(None,uid,connection, cursor) 
        main.pages(uid,connection, cursor).session_id = sno
        print("New sno created ",sno)
        #Assumed that the session number is returned 
    else:
        sno = sessionExist[0][0]
        print("Session: ",sno)
  
    cursor.execute('''SELECT *
                    FROM listen 
                    WHERE uid = ?
                    AND sid = ?
                    AND sno = ?;''', (uid,sid,sno))
    songExist = cursor.fetchall()
    #You can assume the user cannot have more than one active session.
    # print(songExist[0])
    # print(songExist[0])
    # if songExist!= 0:
    # print(songExist)
    # print(len(songExist))
    if len(songExist) != 0:
        cursor.execute('''UPDATE listen 
                        SET cnt=cnt+1 
                        WHERE uid=? 
                        AND sid=? 
                        AND sno=?''', (uid,sid,sno))
        connection.commit()
        print("Update compeleted!")
    else:
        cursor.execute('''INSERT INTO listen VALUES (?, ?, ?, ?)''', (uid,sno,sid,1))
        connection.commit()
        print("Insert compeleted!")
    print("Listening to Song")
    songAction(sid,uid,connection, cursor)
    return

def addToPL(sid, uid,connection, cursor):
    #This function  adds this song (sid) to an existing playlist owned by the user (if any) or to a new playlist.
    #Can have same song multiple time in the playlist
    playlist = input("Enter the name of the plylist you wan to add to") 
    print("It will create a newplaylist of it doesn't exist or will add to the given playlist name")
    # Forum: Yes, sid and pid are keys for songs and playlists but the titles can be the same.
    checkSong = '''SELECT pid FROM playlists
                    WHERE title LIKE ? 
                    AND uid = ?;'''
    songExist = cursor.execute(checkSong, (playlist,uid))
    songExist = cursor.fetchall()
    if len(songExist)!=0:
        pid = songExist[0][0]
        cursor.execute('''SELECT MAX(sorder) 
                        FROM plinclude 
                        WHERE pid=:PID;''',{"PID":pid})

        sorderOR = cursor.fetchone()
        print(sorderOR)
        print(sorderOR[0])
        if sorderOR[0] != None:
            sorder = int(sorderOR[0]) + 1
        else:
            sorder = 1
        print(sorder)
        try:
            cursor.execute('''INSERT INTO plinclude VALUES (?, ?, ?)''',(pid,sid,sorder))
            print("Song inserted to the playlist")
        except:
            print("Song already in the playlist")
        connection.commit()
    else:
        #New playlist
        # print(cursor.fetchall())
    
        cursor.execute('''SELECT MAX(pid) 
                        FROM playlists;''')
        maxPid = cursor.fetchone()
        # print(maxPid)
        # print(maxPid[0])
        if maxPid[0] != None:
            pid = int(maxPid[0]) + 1
        else:
            pid = 1
        newsorder = 1
        cursor.execute('''INSERT INTO playlists VALUES (?, ?, ?)''',(pid,playlist,uid))
        connection.commit()
        cursor.execute('''INSERT INTO plinclude VALUES (?, ?, ?)''',(pid,sid,newsorder))
        connection.commit()
        print("Song added to playlist")
        songAction(sid,uid,connection, cursor)
    return

def songAction(sid, uid,connection, cursor):
    # This function displays all action that can be performed on a song by a user and also provides option to go to user menu, logout or quit the program.
    print("Please select a number between 1 to 6 as desceibed below):")
    print('1. Listen to this song.')
    print('2. More information.')
    print('3. Add to playlist.')
    print('4. Go to home page')
    print('5. Logout')
    print('6. Exit')
    cmd = input()
    if cmd == '1':
        listen(sid,uid,connection, cursor) 
        return
    elif cmd == '2':
        print("info")
        info(sid,uid,connection, cursor)
        return
    elif cmd == '3':
        addToPL(sid,uid,connection, cursor)
        return
    elif cmd == '4':
        p = main.pages(uid,connection, cursor)
        p.home()
        return
    elif cmd == '5':
        main.logout(uid)
        return
    elif cmd == '6':
        exit()
        return
    
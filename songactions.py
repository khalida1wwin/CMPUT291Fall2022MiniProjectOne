import sqlite3
import string

connection = None
cursor = None

def info(sid,uid):
    # More information for a song is the names of artists who performed it 
    # in addition to id, title and duration of the song as well as the names of 
    # playlists the song is in (if any).
    global connection, cursor
    print("Song Details\n")
    cursor.execute('''SELECT sid, title, duration 
                    FROM songs 
                    WHERE sid = ?''', sid)
    all_entry = cursor.fetchall()
    for one_entry in all_entry:
        print(one_entry)
    print("Artist Details\n")
    cursor.execute('''SELECT a.name
                    FROM perform p, artists a
                    WHERE p.sid = ?
                    AND a.aid = p.aid''', sid)
    artists = cursor.fetchall()
    for one_entry in artists:
        print(one_entry)
    print("Playlist Details\n")
    cursor.execute('''SELECT p.title 
                    FROM playlists p, plinclude pl
                    WHERE pl.pid = p.pid 
                    AND pl.sid = ?''', sid)
    playlist = cursor.fetchall()
    for one_entry in playlist:
        print(one_entry)
    songAction(sid,uid) # Go back to the menu after everything is done??
    return

def listen(sid, uid):
    global connection, cursor
    checkSession = '''SELECT sno FROM sessions
                    WHERE uid LIKE ? 
                    AND end IS NULL;'''
    sessionExist = cursor.execute(checkSession, uid)
    sessionExist = cursor.fetchone()
    if(len(sessionExist)==0):
        sno = startSession(uid) 
        #Assumed that the session number is returned 
    else:
        sno = checkSession[0]
        checkSong = '''SELECT *
                       FROM listen 
                       WHERE uid LIKE ?
                       AND sid = ?
                       AND sno = ?'''
        songExist = cursor.execute(checkSong, (uid,sid,sno))
        songExist = cursor.fetchone()
        #You can assume the user cannot have more than one active session.
        if len(songExist)!=0:
            cursor.execute= ('''UPDATE listen 
                            SET cnt=cnt+1 
                            WHERE uid=? 
                            AND sid=? 
                            AND sno=?''', (uid,sid,sno))
            connection.commit()
        else:
            cursor.execute('''INSERT INTO listen VALUES (?, ?, ?, 1)''', (uid,sid,sno))
            connection.commit()
    print("Listening to Song")
    songAction(sid,uid)
    return

def addToPL(sid, uid):
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
                        WHERE pid= ?;''',pid)
        sorder = cursor.fetchall()[0][0] + 1
        cursor.execute('''INSERT INTO plinclude VALUES (?, ?, ?)''',(pid,sid,sorder))
        connection.commit()
    else:
        #New playlist
        cursor.execute('''SELECT MAX(pid) 
                        FROM playlist
                        WHERE uid= ?;''',uid)
        pid = cursor.fetchall()[0][0] + 1
        newsorder = 1
        cursor.execute('''INSERT INTO playlist VALUES (?, ?, ?)''',(pid,playlist,uid))
        connection.commit()
        cursor.execute('''INSERT INTO plinclude VALUES (?, ?, ?)''',(pid,sid,newsorder))
        connection.commit()
        songAction(sid,uid)
    return

def songAction(sid, uid):
    print("Please select a number between 1 to 6 as desceibed below):\n ")
    print('1. Listen to this song.\n')
    print('2. More information.\n')
    print('3. Add to playlist.\n')
    print('4. Menu\n')
    print('5.Logout\n')
    print('6.Exit\n')
    cmd = int(input())
    if cmd == '1':
        listen(sid,uid) 
        return
    elif cmd == '2':
        info(sid,uid)
        return
    elif cmd == '3':
        addToPL(sid,uid)
        return
    elif cmd == '4':
        menu()
        return
    elif cmd == '5':
        logout()
        return
    elif cmd == '6':
        exit()
        return
    

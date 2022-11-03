import sqlite3
import string

connection = None
cursor = None
# Add comments later, Check if query works, check if the inputs are same 
def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def addSong(aid):
    global connection, cursor
    title= map(string, input("Enter the song title: "))
    while title:
    #loops till a positive integer is entered after the title is entered
        try:
            duration = int(input("Enter the song duration: "))
            assert duration > 0
        except AssertionError:
            print("Error! Please input a positive number.")
            continue
        break
    artists = list(map(str, input("Enter the ids of additional artists (separated by space). If none, enter space: ").split()))
    if aid not in artists:
        artists.append(aid) #Adding the current artist aid to the list of all artist performing the song
        
    cursor.execute('''SELECT aid FROM artists''')
    artist_aid= cursor.fetchall()
    for i in artists:
        if i not in artist_aid:
            print("Error! The artist aid" + i + "does not exist")
            addSong(aid)
            return

    checkSong = ('''SELECT * 
                  FROM songs s
                  WHERE s.title LIKE ?
                  AND s.duration = ?''')
    songExist = cursor.execute(checkSong, (title, duration))
    songExist = cursor.fetchone()
    cursor.execute('''SELECT MAX(s.sid) 
                    FROM songs s;''')
    newsid = cursor.fetchall()[0][0] + 1
    if (songExist):
        print("This song already exists in the database")
        artistAction(aid)
    else:
        print("continue to add a song")
        cursor.execute('''INSERT INTO songs VALUES(?, ?, ?)''', (newsid, title, duration))
        cursor.commit()
    
    for i in artists:
        cursor.execute('INSERT INTO perform VALUES(?, ?)', (i, newsid))
        connection.commit()
    ##adding additional performers
    
    return

def topFans(aid):
    global connection, cursor
    print("Top 3 Fans are:\n")
    cursor.execute('''SELECT u.name, SUM(l.cnt * s.duration) 
                    FROM listen l, perform p, user u, songs s, artists a
                    WHERE p.aid= ?
                    AND l.sid = s.sid 
                    AND s.sid = p.sid
                    AND p.aid = a.aid
                    AND l.uid = u.uid
                    GROUP BY l.uid, p.aid
                    ORDER BY SUM(l.cnt * s.duration) DESC
                    LIMIT 3;''', aid)
    all_entry = cursor.fetchall()
    for one_entry in all_entry:
        print(one_entry)
    return

def topPlaylist(aid):
    global connection, cursor
    print("Top 3 Playlists are:\n")
    cursor.execute('''SELECT pli.pid, pli.title, COUNT(*)
                    FROM perform p, plinclude pli, playlists pl
                    WHERE p.aid = ?
                    AND p.sid = pli.sid
                    AND pl.pid = pli.pid
                    GROUP BY pli.pid
                    ORDER BY COUNT(*) DESC
                    LIMIT 3''',aid)
    all_entry = cursor.fetchall()
    for one_entry in all_entry:
        print(one_entry)
    return

def artistAction(aid):
    print("Please select a number between 1 to 4 as desceibed below):\n ")
    print("1. Add a song \n2. Find top fans and playlists \n3. Log out \n4. Quit the program")
    cmd = int(input())
    if cmd == 1:
        addSong(aid)
        return 
        
    elif cmd == 2:
        topFans(aid)
        topPlaylist(aid)
        return 
    
    elif cmd == 3:
        logout()
        print("Logout Successful")
        return False, False

    elif cmd == 4:
        exit()
    else:
        print("Incorrect input.")
    

def main():
    global connection, cursor
    path="./test.db"
    connect(path)

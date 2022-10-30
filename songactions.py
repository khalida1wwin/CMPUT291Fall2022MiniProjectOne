import sqlite3
import string

connection = None
cursor = None

def info(aid_from_songs):
    global connection, cursor
    cursor.execute(''' SELECT s.sid, s.title, s.duration 
                            FROM artists a, songs s, perform p
                            WHERE a.aid = :artist_num
                            AND a.aid = p.aid
                            AND p.sid = s.sid
                            GROUP BY s.sid
                        ''', {'artist_num': aid_from_songs})
    artist_info = cursor.fetchall()
    return
def songAction(song):
    print("Please select a number between 1 to 6 as desceibed below):\n ")
    print('1. Listen to this song.\n')
    print('2. More information.\n')
    print('3. Add to playlist.\n')
    print('4. Menu\n')
    print('5.Logout\n')
    print('6.Exit\n')
    cmd = int(input())
    if cmd == '1':
        listenSong(song) 
        return
    elif cmd == '2':
        info(aid_from_songs)
        return
    elif cmd == '3':
        addtoPL()
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
    

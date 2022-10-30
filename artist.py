import sqlite3
import string

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def addSong(aid):
    global connection, cursor
    title, duaration = map(string, input("Please enter a title and duration in format(title, duration): ").split())
    checkSong = '''SQL exist in query '''
    songExist = cursor.execute(checkSong)
    songExist = cursor.fetchall()
    if (songExist):
        print("Song already exists in the database")
    else:
        print("continue to add a song")
        cursor.execute('''SQL add song query ''')
        cursor.commit()
        ##adding additional performers
    return

def topFans():
    global connection, cursor
    print("Top 3 Fans are:\n")
    cursor.execute('''SQL top 3 fans query''')
    all_entry = cursor.fetchall()
    for one_entry in all_entry:
        print(one_entry)
    return

def topPlaylist(aid):
    global connection, cursor
    print("Top 3 Playlists are:\n")
    cursor.execute('''SQL top 3 playlist query''')
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

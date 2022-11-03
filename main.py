import maskpass 
import sqlite3
class user():
    def __init__(self):
        pass
    def login(self):
        # login
        self.UID = input("Enter your new user id: ")
        self.password = maskpass.askpass(mask="")
        # print("passwor",self.password )
        #TODO: check if the user in the DB
        # return bool val if correct and user id and password exist
        # in DB
        # if user in the DB
        # return self.UID
    def signup(self):
        # signup
        # login
        self.UID = input("Enter your new user id: ")
        self.userName = input("Enter your name: ")
        self.password = maskpass.askpass(mask="")
        print("passwor",self.password ) 
        #TODO if UID exist in DB ask again the user of new UID
        # if UID exist doesn't exist then return uid
        return self.UID
    def logout(self):
        # logout
        pass
class pages():
    def __init__(self,uid):
        self.uid = uid
    def home(self):
        print("Welcome ",  self.uid)
        print("What do you want to do (select number)?")
        print("1. Start a session")
        print("2. Search for songs and playlists.")
        print("3. Search for artists.")
        print("4. End the session.")
        print("5. Log Out")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.StartSession()
        elif choice == "2":
            self.searchSongsAndPlaylists()
        elif choice == "3":
            self.playlist()
        elif choice == "4":
            self.setting()
        elif choice == "5":
            self.logout()
        elif choice == "6":
            exit()
    def searchSongsAndPlaylists(self):
        pass
    def Searchplaylist(self):
        pass
    def StartSession(self):
        pass
    def setting(self):
        pass
    def logout(self):
        pass

def main():
    path="./mini.db"
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()


    while True:
        print("Welcome to the songs App!")
        inp1  = input("Are you an artists(a) or user(u): ")
        # print(inp)
        if inp1  == "u":
            print("Welcome User")
            print("Choose option: ")
            print("1. Log in")
            print("2. Sign up")
            print("3. Exit")
            inp2  = input()
            if inp2  == "1":
                print("Log in")
                # login
                user1 = user()
                uid = user1.login()
                p = pages()
                print(uid)
                p.home(uid)
            elif  inp2  == "2":
                print("Sign up")
                # signup
                user1 = user()
                user1.signup()
                p = pages()
                p.home()
            elif  inp2  == "3":
                print("Exit")
                break
        elif inp1  == "a":
            print("Welcome Artisit ")
            print("Choose option: ")
            print("1. Log in")
            print("2. Exit")
            inp2  = input()
            if inp2  == "1":
                print("Log in")
                # login
                user1 = user()
                uid = user1.login()
                p = pages()
                p.home(uid)
            elif  inp2  == "2":
                print("Exit")
                break

        else:
            print("Invalid input")
            continue

main()


###############################
# import sqlite3
# import string

# connection = None
# cursor = None

# def connect(path):
#     global connection, cursor
#     connection = sqlite3.connect(path)
#     cursor = connection.cursor()
#     cursor.execute(' PRAGMA forteign_keys=ON; ')
#     connection.commit()
#     return

# def addSong(aid):
#     global connection, cursor
#     title, duaration = map(string, input("Please enter a title and duration in format(title, duration): ").split())
#     checkSong = '''SQL exist in query '''
#     songExist = cursor.execute(checkSong)
#     songExist = cursor.fetchall()
#     if (songExist):
#         print("Song already exists in the database")
#     else:
#         print("continue to add a song")
#         cursor.execute('''SQL add song query ''')
#         cursor.commit()
#         ##adding additional performers
#     return

# def topFans():
#     global connection, cursor
#     print("Top 3 Fans are:\n")
#     cursor.execute('''SQL top 3 fans query''')
#     all_entry = cursor.fetchall()
#     for one_entry in all_entry:
#         print(one_entry)
#     return

# def topPlaylist(aid):
#     global connection, cursor
#     print("Top 3 Playlists are:\n")
#     cursor.execute('''SQL top 3 playlist query''')
#     all_entry = cursor.fetchall()
#     for one_entry in all_entry:
#         print(one_entry)
#     return

# def artistAction(aid):
#     print("Please select a number between 1 to 4 as desceibed below):\n ")
#     print("1. Add a song \n2. Find top fans and playlists \n3. Log out \n4. Quit the program")
#     cmd = int(input())
#     if cmd == 1:
#         addSong(aid)
#         return 
        
#     elif cmd == 2:
#         topFans(aid)
#         topPlaylist(aid)
#         return 
    
#     elif cmd == 3:
#         logout()
#         print("Logout Successful")
#         return False, False

#     elif cmd == 4:
#         exit()
#     else:
#         print("Incorrect input.")
    

# def main():
#     global connection, cursor
#     path="./test.db"
#     connect(path)

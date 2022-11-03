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
    def logout(self,uid):
        # logout
        self.UID = None
        self.password = None
        exit()

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
            self.SearchForArtists()
        elif choice == "4":
            self.setting()
        elif choice == "5":
            self.logout()
        elif choice == "6":
            exit()
    def searchSongsAndPlaylists(self):
        earch = input("What do you want to search for? (seprate keywords with comma)")
        print("=> search results : (playlist name or song name)")
        print("⇒ ID , the title, the duration, song / playlist : order by no. of keywords found till 1: top 5 matches")
        print("What do you what to do (select number)?")
        print("1. See more search result")
        print("2. Enter the result no")
        print("3. Go to home page")
        print("4. Log Out")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.moreSearchResult()
        elif choice == "2":
            self.SelectResult()
        elif choice == "3":
            self.home()
        elif choice == "4":
            self.logout()
        elif choice == "5":
            exit()
    def SearchForArtists(self):
        search = input("What do you want to search for? (seprate keywords with comma)")
        print("=> search results : (playlist name or song name)")
        print("⇒ ID , the title, the duration, song / playlist : order by no. of keywords found till 1: top 5 matches")
        print("What do you what to do (select number)?")
        print("1. See more search result")
        print("2. Select result")
        print("3. Go to home page")
        print("4. Log Out")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.moreSearchResult()
        elif choice == "2":
            self.SelectResult()
        elif choice == "3":
            self.home()
        elif choice == "4":
            self.logout()
        elif choice == "5":
            exit()
    def StartSession(self):
        print("Session #:")
        print("Session start date: xx/x/xxxx")
        print("What do you want to do (select number)?")
        print("1. Go to home page")
        print("2. Log Out")
        print("3. Exit ")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.home()
        elif choice == "2":
            self.logout()
        elif choice == "3":
            exit()
    def moreSearchResult(self):
        pass
    def SelectResult(self):
        pass
    def logout(self):
        self.uid = None
        exit()

def main():
    path="./mini.db"
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()


    while True:
        curr_id = None
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
                curr_id = user1.login()
                p = pages(curr_id)
                print(curr_id)
                p.home()
            elif  inp2  == "2":
                print("Sign up")
                # signup
                user1 = user()
                curr_id = user1.signup()
                p = pages(curr_id)
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
                p.home()
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

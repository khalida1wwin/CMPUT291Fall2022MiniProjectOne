import maskpass 
import sqlite3
class user():
    def __init__(self):
        pass
    def login(self,UORA):
        # login
        if UORA == "U":
            while True:
                self.UID = input("Enter your user id: ")
                self.password = maskpass.askpass(mask="")
                # print("passwor",self.password )
                #TODO: check if the user in the DB
                # return bool val if correct and user id and password exist
                # in DB
                # if user in the DB
                checkUser = ('''
                SELECT EXISTS(SELECT * FROM users WHERE uid = ? AND pwd = ?)''')
                userExist = cursor.execute(checkUser,(self.UID,self.password))
                userExist = userExist.fetchone()
                if userExist[0]:
                    print("successful log in")
                    connection.commit()
                    return self.UID
                else:
                    print("user does not exist")
                    
        elif UORA == "A":
            while True:
                self.aid = input("Enter your artist id: ")
                self.password = maskpass.askpass(mask="")
                # print("passwor",self.password )
                checkUser = ('''
                SELECT EXISTS(SELECT * FROM artists WHERE aid = ? AND pwd = ?)''')
                userExist = cursor.execute(checkUser,(self.aid,self.password))
                userExist = userExist.fetchone()
                if userExist[0]:
                    print("successful log in")
                    connection.commit()
                    return self.aid
                else:
                    print("artist does not exist")

        # return self.UID
    def signup(self):
        # signup
        # login
        while True:
            self.UID = input("Enter your new user id: ")
            self.userName = input("Enter your name: ")
            self.password = maskpass.askpass(mask="")
            # print("password",self.password ) 
            #TODO if UID exist in DB ask again the user of new UID
            # if UID exist doesn't exist then return uid
            checkUser = ('''
                SELECT EXISTS(SELECT * FROM users WHERE uid=:newUID)''')
            userExist = cursor.execute(checkUser,{"newUID":self.UID})
            userExist = userExist.fetchone()
            if userExist[0]:
                print("userlog in")
                connection.commit()
                print("please try new user id")
                # return self.UID
            else:
                newUser = ('''
                INSERT INTO users(uid,name,pwd) VALUES(?,?,?)''')
                cursor.execute(newUser,(self.UID,self.userName,self.password))
                connection.commit()
                print("successful sign up")
                return self.UID
    def logout(self,uid):
        # logout
        self.UID = None
        self.password = None
        # exit()

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
                curr_id = user1.login("U")
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
                curr_id = user1.login("A")
                p = pages(curr_id)
                p.home()
            elif  inp2  == "2":
                print("Exit")
                break

        else:
            print("Invalid input")
            continue
main()

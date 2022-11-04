import maskpass 
import sqlite3
import artist
import userAction
import songactions
class user():
    def __init__(self,connection, cursor):
        self.connection = connection
        self.cursor = cursor
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
                    self.connection.commit()
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
            userExist = self.cursor.execute(checkUser,{"newUID":self.UID})
            userExist = userExist.fetchone()
            if userExist[0]:
                print("userlog in")
                self.connection.commit()
                print("please try new user id")
                # return self.UID
            else:
                newUser = ('''
                INSERT INTO users(uid,name,pwd) VALUES(?,?,?)''')
                cursor.execute(newUser,(self.UID,self.userName,self.password))
                self.connection.commit()
                print("successful sign up")
                return self.UID
    def logout(self,uid):
        # logout
        logout(uid)
        # exit()

class pages():
    def __init__(self,uid,connection, cursor):
        self.cursor = cursor
        self.connection = connection
        self.uid = uid
        self.session_id = None
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
            userInput = input("Do you want to search for songs(s) or playlists(p)?")
            if userInput == "s":
                userAction.searchSongs(self.session_id,self.uid,self.connection,self.cursor)
            elif userInput == "p":
                userAction.searchPlaylists(self.session_id,self.uid,self.connection,self.cursor)
            else:
                print("invalid input")
                self.home()

        elif choice == "3":
            self.SearchForArtists()
        elif choice == "4":
            self.EndSession()
        elif choice == "5":
            self.logout()
        elif choice == "6":
            exit()
    def searchSongsAndPlaylists(self):
        userAction.searchSongs(self.session_id,self.uid,self.connection,self.cursor)
        # print("=> search results : (playlist name or song name)")
        # print("⇒ ID , the title, the duration, song / playlist : order by no. of keywords found till 1: top 5 matches")
        # self.home()
    def SearchForArtists(self):
        userAction.searchArtists(self.session_id,self.uid,self.connection,self.cursor) 
        # print("=> search results : (playlist name or song name)")
        # print("⇒ ID , the title, the duration, song / playlist : order by no. of keywords found till 1: top 5 matches")
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
        self.session_id, startDate = userAction.session_start(self.session_id,self.uid,self.connection,self.cursor)
        print("Session:",self.session_id)
        print("Session start date:",startDate)
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
    def EndSession(self):
        self.session_id = userAction.end_session(self.session_id,self.uid,self.connection,self.cursor)
        
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
    def songAction(self,sid, uid,connection, cursor):
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
            self.listen(sid,uid,connection, cursor) 
            return
        elif cmd == '2':
            print("info")
            self.info(sid,uid,connection, cursor)
            return
        elif cmd == '3':
            self.addToPL(sid,uid,connection, cursor)
            return
        elif cmd == '4':
            # p = pages(uid,connection, cursor)
            p.home()
            return
        elif cmd == '5':
            logout(uid)
            return
        elif cmd == '6':
            exit()
    def listen(sid, uid,connection, cursor):
    #This function updates the listen count if a song is already listened to in a session. It inserts
    # a listen event to the session if the song is not listened to in the session. It creates a new session, if there is no existing one.
        checkSession = '''SELECT sno FROM sessions
                        WHERE uid=:UID 
                        AND end IS NULL;'''
        cursor.execute(checkSession, {"UID":uid})
        sessionExist = cursor.fetchall()
        print(sessionExist)
        if len(sessionExist) == 0:
            self.session_id,Date = userAction.session_start(None,uid,connection, cursor) 
            print("New sno created",sno)
            #Assumed that the session number is returned 
        else:
            sno = sessionExist[0][0]
            print(sno)
    
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
        self.songAction(sid,uid,connection, cursor)
        return
    def logout(self):
        self.session_id = userAction.end_session(self.session_id,self.connection, self.cursor)
        self.uid = None


if __name__ == "__main__":
    path="./mini.db"
    global connection, cursor, curr_id
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit(),connection, cursor
    curr_id = None
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
                user1 = user(connection, cursor)
                curr_id = user1.login("U")
                p = pages(curr_id,connection, cursor)
                print(curr_id)
                p.home()
            elif  inp2  == "2":
                print("Sign up")
                # signup
                user1 = user(connection, cursor)
                curr_id = user1.signup()
                p = pages(curr_id,connection, cursor)
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
                user1 = user(connection, cursor)
                curr_id = user1.login("A")
                p = pages(curr_id,connection, cursor)

                artist.artistAction(curr_id,connection, cursor)

            elif  inp2  == "2":
                print("Exit")
                break

        else:
            print("Invalid input")
            continue

def logout(uid):
    # logout
    global curr_id
    curr_id = None




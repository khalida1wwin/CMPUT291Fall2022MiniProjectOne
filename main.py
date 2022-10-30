import maskpass 

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
        # return self.UID
    def logout(self):
        # logout
        pass
# class pages():
#     def __init__(self,uid):
#         self.uid = uid
#     def home(self):
#         print("Welcome ",  self.uid)
#         print("What do you want to do (select number)?")
#         print("1. Start a session")
#         print("2. Search for songs and playlists.")
#         print("3. Search for artists.")
#         print("4. End the session.")
#         print("5. Log Out")
#         print("6. Exit")
#         choice = input("Enter your choice: ")
#         if choice == "1":
#             self.StartSession()
#         elif choice == "2":
#             self.searchSongsAndPlaylists()
#         elif choice == "3":
#             self.playlist()
#         elif choice == "4":
#             self.setting()
#         elif choice == "5":
#             self.logout()
#         elif choice == "6":
#             exit()
#     def searchSongsAndPlaylists(self):
#         pass
#     def Searchplaylist(self):
#         pass
#     def StartSession(self):
#         pass
#     def setting(self):
#         pass
#     def logout(self):
#         pass

def main():
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
                user1.login()
            elif  inp2  == "2":
                print("Sign up")
                # signup
                user1 = user()
                user1.signup()
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
                user1.login()
            elif  inp2  == "2":
                print("Exit")
                break

        else:
            print("Invalid input")
            continue

main()
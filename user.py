from ast import While
from cProfile import run
import sqlite3
import sys
import random
import time
import getpass
from datetime import datetime


conn = None
c = None
my_id = None
my_sid = None
my_mid = None
movie_start_time = None

def main():
    # Menu that prompts the users for an action relating to sign in
	db_path = './' + sys.argv[1]
	connect(db_path)
	while True:
		option = prompt_options()
		if option == 's':
			sign_up()
			customer_menu()
		elif option == 'c':
			customer_login()
			customer_menu()
		elif option == 'e':
			editor_login()
			editor_menu()
		elif option == 'q':
			conn.commit()
			conn.close()
			break

def connect(path):
    global conn, c

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    conn.commit()
    return

def prompt_options():
	while True:
		print("Enter 'c' for customer login")
		print("Enter 'e' for editor login")
		print("Enter 's' to sign up")
		print("Enter 'q' to quit")
		entry = input()
		if entry in 'cesq' and len(entry) == 1:
			return entry

def sign_up():
    #function that adds in data of the customer who signed up
	global conn, c, my_id

	while True:
		cid = input('cid: ')
		name = input('name: ')
		pwd = getpass.getpass()
		try:
			c.execute("INSERT INTO customers VALUES (?, ?, ?);", (cid, name, pwd))
			conn.commit()
			print('Registration succeeded')
			my_id = cid
			return
        #error handled if the customer already has an account
		except sqlite3.Error as e:
			print(e)

def customer_login():
	global conn, c, my_id

	while True:
		cid = input('Enter cid: ')
		pwd = getpass.getpass()
		c.execute("SELECT * FROM customers WHERE UPPER(cid) = ? AND pwd = ?;", (cid.upper(), pwd))
		if len(c.fetchall()) == 1:
			print('Login succeeded')
			my_id = cid
			return
		else:
			print("Login failed")

def editor_login():
	global conn, c, my_id

	while True:
		eid = input('Enter eid: ')
		pwd = getpass.getpass()
		c.execute('SELECT * FROM editors WHERE UPPER(eid) = ? AND pwd = ?;', (eid.upper(), pwd))
		if len(c.fetchall()) == 1:
			print('Login succeeded')
			my_id = eid
			return
		else:
			print("Login failed")


def customer_menu():
	global my_sid, my_id, my_mid
    #Menu shown to customer after a successfull authentication

	while True:
		print('Select a task:')
		print('1. Start a session')
		print('2. Search for movies')
		print('3. End watching a movie')
		print('4. End the session')
		print('5. Log out')
		option = input()
		if option == '1':
			startSession()
		elif option == '2':
			search_movies()
		elif option == '3':
			end_movie()
		elif option == '4':
			end_session()
		elif option == '5':
			if my_sid != None:
				end_session()
			my_id = None
			break
		
		#elif option == '2':
		#elif option == '3':

		#elif option == '4':	
	
def editor_menu():
	global my_id
    #Menu shown to editor after a successfull authentication

	while True:
		print('Select a task:')
		print('1. Add a movie')
		print('2. Update a recommendation')
		print('3. Log out')
		option = input()
		if option == '1':
			editor_add()
		elif option == '2':
			update_recommendation()
		elif option == '3':
			my_id = None
			break
	
def startSession():
	global my_sid,conn, c

	if my_sid == None:
		while True:
            # assigning a unique sid to the session
			random_sid = int(random.randint(0,1000))
			c.execute('SELECT COUNT(sid) FROM sessions WHERE sid=? AND cid=?;',(random_sid,my_id))
			rand_sid_count = c.fetchone()[0]
			my_sid = random_sid
			
			now = datetime.now()
			
			start_date = now.strftime("%Y-%m-%d %H:%M:%S")
			
			data = (random_sid, my_id, start_date)
			#ensuring the sid is unique
			if rand_sid_count > 0:
				print("Not a unique sid")
				my_sid = None
			else:
				c.execute('INSERT INTO sessions (sid,cid,sdate,duration) VALUES (?,?,?,NULL);',data)
				conn.commit()
				break
	else:
		print("You must end the current session before starting a new session")
	
def end_movie():
	global my_id, movie_start_time, c, conn, my_sid, my_mid
    #Records the duration of long the movie has been watched


	if my_mid != None:
		current_time = time.time()		
		duration_sec = current_time - movie_start_time		
		duration_mins = round(duration_sec / 60)		
		c.execute('SELECT m.title FROM movies as m, watch as w WHERE m.mid = w.mid AND UPPER(cid)=? AND sid=? AND w.mid=?;',(my_id.upper(),my_sid,my_mid))
		
		movie_title = c.fetchone()[0]
		
		c.execute('SELECT runtime FROM movies WHERE mid=?;',(my_mid,))
		run_time = c.fetchone()[0]
	
		if duration_mins <= run_time:
			c.execute('UPDATE watch SET duration=? WHERE UPPER(cid)=? AND sid=? AND mid=?;',(duration_mins,my_id.upper(),my_sid,my_mid))
			my_mid= None
			movie_start_time= None
			conn.commit()
		else:
			print("Cannot end watching movie. Duration watched exceeds runtime")
	else:
		print("Cannot end a movie that has not been started")
	
		

def end_session():
	global my_sid, my_id, c, conn

	data = (my_id.upper(),my_sid)
    
    #check to see if the movie has been started
	if movie_start_time != None:
		end_movie() 


	if my_sid == None:
		print("You cannot end a session that has not been started")
	else:
		c.execute('SELECT sdate FROM sessions WHERE UPPER(cid)=? AND sid=?;',data)
		start_date = c.fetchone()[0]
		start_dateObj = datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
		
		now = datetime.now()
		current_date = now.strftime("%Y-%m-%d %H:%M:%S")
		current_dateObj = datetime.strptime(current_date,'%Y-%m-%d %H:%M:%S')
		
		time_diff = (current_dateObj - start_dateObj)
		
		total_seconds = time_diff.total_seconds()
		
		minutes= round(total_seconds / 60)
		
		c.execute('UPDATE sessions SET duration=? WHERE sid=? AND UPPER(cid)=?;',(minutes,my_sid,my_id.upper()))
		my_sid = None

		conn.commit()


def search_movies():
	global conn, c

	keywords = input('Please enter one or more keywords separated by a space: ').split()
	if len(keywords) == 0:
		return
	movie_query = "SELECT DISTINCT m.mid, title, year, runtime FROM movies m, casts c, moviePeople WHERE m.mid = c.mid AND c.pid = moviePeople.pid"
	i = 1
	for keyword in keywords:
		if i == 1:
			movie_query += " AND (title LIKE '%{0}%' OR role like '%{1}%' OR name like '%{2}%')".format(keyword, keyword, keyword)
		else:
			movie_query += " OR (title LIKE '%{0}%' OR role like '%{1}%' OR name like '%{2}%')".format(keyword, keyword, keyword)
		i += 1
	movie_query += " ORDER BY ("
	for keyword in keywords:
		movie_query += "CASE WHEN title LIKE '%{0}%' THEN 1 ELSE 0 END + CASE WHEN role like '%{1}%' THEN 1 ELSE 0 END + CASE WHEN name like '%{2}%' THEN 1 ELSE 0 END + ".format(keyword, keyword, keyword)
	movie_query = movie_query.rstrip("+ ")
	movie_query += ") DESC;"
	if sqlite3.complete_statement(movie_query):
		c.execute(movie_query)
		movies = c.fetchall()
		if len(movies) == 0:
			print('No search results')
			return
		if len(movies) < 6:
			for i in range(len(movies)):
				print(i+1, movies[i])
			while True:
				entry = input('Select a movie: ')
				if entry.isnumeric():
					break
			movie_screen(movies[int(entry)-1])
		else:
			for i in range(len(movies)):
				if i > 4:
					while True:
						entry = input('Select movie or press enter to see more matches: ')
						if entry.isnumeric() or len(entry) == 0:
							break
					if len(entry) == 0:
						for j in range(5, len(movies)):
							print(j+1, movies[j])
						while True:
							movie_index = input('Select a movie: ')
							if movie_index.isnumeric():
								break
						movie_screen(movies[int(movie_index)-1])
						break
					else:
						movie_screen(movies[int(entry)-1])
						break
				print(i+1, movies[i])
	else:
		print("Cannot execute movie query")

# movie is a tuple containing the mid, title, year, and runtime
def movie_screen(movie):
    # prints out the details about the selected movie
	global conn, c, my_id, movie_start_time, my_sid, my_mid

	c.execute("SELECT * FROM movies m WHERE m.mid = ?;", (movie[0],))
	print(c.fetchone())

	c.execute("SELECT COUNT(DISTINCT cid) FROM watch w, movies m WHERE w.mid = m.mid AND duration*2 >= runtime AND m.mid = ?;", (movie[0],))
	print("Number of customers who have watched:", c.fetchone()[0])

	c.execute("SELECT c.pid, name, birthYear FROM movies m, casts c, moviePeople WHERE m.mid = c.mid AND c.pid = moviePeople.pid AND m.mid = ?;", (movie[0],))
	cast_members = c.fetchall()
	print("Cast members:")
	for i in range(len(cast_members)):
		print(i+1, cast_members[i])
	while True:
		entry = input("Select a cast member to follow or enter 'watch' to start watching: ")
		if entry.isnumeric():
			try:
				c.execute("INSERT INTO follows VALUES (?, ?);", (my_id, cast_members[int(entry)-1][0]))
				conn.commit()
				print("Followed")
			except sqlite3.Error as e:
				print(e)
		elif entry == 'watch':
			if my_sid != None and my_mid == None and movie_start_time == None:
				c.execute("INSERT INTO watch VALUES (?, ?, ?, NULL);", (my_sid, my_id, movie[0]))
				conn.commit()
				movie_start_time = time.time()
				my_mid = movie[0]
				print("Now watching", movie[1])
			elif my_sid == None:
				print("You need to start a session first")
			else:
				print("You are already watching a movie")
			return

def editor_add():
    data = input(
        "Enter movieID, title, year, runtime seperated by a comma: ").split(sep=",")
    moviedata = (int(data[0]), data[1], int(data[2]), int(data[3]))
    c.execute("Select count(*) from movies where mid = :movieID;",{'movieID':data[0]})
    movie_count = c.fetchone()[0]
    
    #inserts the movie, only if the entered movieID is unique
    if movie_count == 0:        
        c.execute(
            'INSERT INTO movies (mid,title,year,runtime) VALUES (?,?,?,?);', moviedata)
        end = 1
        while 1:
            cast_memberID = input(
                "Enter the moviePeople ID to cast them for this movie, or 'Done': ")
            if(cast_memberID == "Done"):
                break
            else:
                #calls a function that takes in the cast members in the movie
                add_cast_member(cast_memberID, int(data[0]))
    else:
        print("There exists a movie with the same movieID, please try another mid")
    conn.commit()


def add_cast_member(cast_memberID, movieID):
    #prints all existing cast members to choose from and gives the editor the option to assign roles to them
    c.execute("SELECT mp.name, mp.birthYear from moviePeople mp where UPPER(mp.pid) = :castID;", {
              "castID": cast_memberID.upper()})
    castmembers = c.fetchall()

    count = 0
    print("Name | Birth Year ")
    for members in castmembers:
        print(members)
        count = count + 1
    #prints all existing cast members to choose from and gives the editor the option to assign roles to them
    if(count > 0):
        selected = input("Enter 'A' to accept, 'R' to reject cast member: ")
        if selected == 'A':
            role = input("Enter a role to assign to this cast member: ")
            cast_data = (movieID, cast_memberID, role)
            c.execute("select count(*) from casts where mid =:mpid and UPPER(pid) =:pid ;",{'mpid':movieID,'pid':cast_memberID.upper()})
            cast_count =c.fetchone()[0]
            if cast_count == 0:
                c.execute(
                'INSERT INTO casts (mid, pid, role) VALUES (?,?,?);', cast_data)
            else:
                print("Cast member cannot act in 2 roles in the same movie")

    #if a new castID is entered, a new cast member is added to table
    else:
        new_cast_member = input("Add new cast member by typing in their ID, name and their birth year:").split(sep=",")
        c.execute("select count(*) from moviePeople where UPPER(pid) =:mpid;",{'mpid':new_cast_member[0].upper()})
        count_mp= c.fetchone()[0]
        if count_mp == 0:
            new_cast_member_data = (
            new_cast_member[0], new_cast_member[1], int(new_cast_member[2]))
            c.execute(
            'INSERT INTO moviePeople (pid,name,birthYear) VALUES (?,?,?);', new_cast_member_data)
        else:
            print("Entered cast member already exist!")

    conn.commit()

def command(m1, m2):
    #adds or deletes movie pairs from the recommendations table
    c.execute("select count(*) from recommendations r where r.watched = :m1 and r.recommended = :m2;",
              {'m1': m1, 'm2': m2})
    movie_in_recommendedlist = c.fetchone()[0]

    print("1. Add/Update recommendation score")
    print("2. Delete recommendation")
    selection = int(input("Enter selection: "))

    if selection == 1:
        newscore = input("Enter new recommendation score for this pair: ")
        #if movie already exits just update
        if movie_in_recommendedlist == 1:           
            c.execute("update recommendations set score = :newscore where watched = :m1 and recommended = :m2;", {
                      'newscore': newscore, 'm1': m1, 'm2': m2})
            print("Recommended score for the movie pair changed")
        #else add to recommendations table
        elif movie_in_recommendedlist == 0:
            new_recomm = (m1,m2,newscore)
            c.execute(
            'INSERT INTO recommendations (watched,recommended,score) VALUES (?,?,?);', new_recomm)
            print("Movie pair inserted to recommendations list")
    
    elif selection == 2:
        c.execute("DELETE from recommendations where watched = :m1 and recommended = :m2;",{'m1':m1,'m2':m2})
        print("Movie pair has been deleted from recommendations list")
    
    conn.commit()


def update_recommendation():
    global conn, c
    print("Select the type of report you require:")
    print("1. Monthly Report")
    print("2. Annual Report")
    print("3. All-time Report")
    t = int(input("Enter report type: "))
    if t==1:
        time = "-30 days"
    elif t==2:
        time = "-365 days"
    else:
        time = "0"

    if time =="-30 days" or time =="-365 days":
        c.execute("""select hh.movieone, hh.movietwo, hh.c, ifnull(r.score,"N/A") from
                  (select m1.mid as movieone, m2.mid as movietwo ,count(distinct c1.cid) as c from sessions s1,
                  customers c1, watch w1, movies m1,sessions s2, customers c2, watch w2, movies m2
                  where c1.cid=w1.cid and w1.mid = m1.mid and w1.sid = s1.sid and w2.sid = s2.sid 
                  and c1.cid=c2.cid and c2.cid=w2.cid and w2.mid = m2.mid AND
                  m1.mid<>m2.mid and w1.duration >= 0.5*m1.runtime
                  and w2.duration >= 0.5*m2.runtime and s1.sdate between datetime('now',:d1) and datetime('now') and s2.sdate
                  between datetime('now',:d1) and datetime('now')
                  group by m1.mid, m2.mid
                  order by count(distinct c1.cid) desc) as hh left outer join recommendations r on hh.movieone = r.watched 
                  and hh.movietwo = r.recommended;
        """,{'d1': time})
    else:
        c.execute("""select hh.movieone, hh.movietwo, hh.c, ifnull(r.score,"N/A") from
                  (select m1.mid as movieone, m2.mid as movietwo ,count(distinct c1.cid) as c from sessions s1,
                  customers c1, watch w1, movies m1,sessions s2, customers c2, watch w2, movies m2
                  where c1.cid=w1.cid and w1.mid = m1.mid and w1.sid = s1.sid and w2.sid = s2.sid 
                  and c1.cid=c2.cid and c2.cid=w2.cid and w2.mid = m2.mid AND
                  m1.mid<>m2.mid and w1.duration >= 0.5*m1.runtime
                  and w2.duration >= 0.5*m2.runtime
                  group by m1.mid, m2.mid
                  order by count(distinct c1.cid) desc) as hh left outer join recommendations r on hh.movieone = r.watched 
                  and hh.movietwo = r.recommended;
        """)

    movie_pairs=c.fetchall()
    print("Movie 1|Movie 2|# of people|Recommendation score")
    for movies in movie_pairs:
        print(movies)

    while 1:
        m = input("Enter a pair of movies to select, seperated by a comma or Done : ",).split(
            sep=",")
        if m[0] == "Done":
            break
        m1 = int(m[0])
        m2 = int(m[1])
        c.execute("""
		    select count(*) from (select m1.mid as n, m2.mid as b,count(distinct c1.cid), ifnull(r.score, 0) from customers c1 left outer join watch w1 on c1.cid=w1.cid left outer join movies m1
                on w1.mid = m1.mid left outer join recommendations r1 on m1.mid=r1.watched, customers c2 left outer join watch w2 on c2.cid=w2.cid left outer join movies m2
                on w2.mid = m2.mid left outer join recommendations r on m2.mid=r.recommended
                where c1.cid=c2.cid and m1.mid<>m2.mid and w1.duration >= 0.5*m1.runtime
                and w2.duration >=0.5*m2.runtime
                group by m1.mid, m2.mid, r1.score
                order by count(distinct c1.cid) desc) hh
                where hh.n = :m1 and hh.b = :m2;
		""", {'m1': m1, 'm2': m2})
        count_movie_pair = c.fetchone()[0]
        #check to see if the entered pair is a movie pair
        if(count_movie_pair == 0):
            print("Entered movies not a pair ")
        
        if(count_movie_pair == 1):
            command(m1, m2)

	
if __name__ == "__main__":
	main()
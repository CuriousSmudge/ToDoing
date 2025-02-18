import sqlite3 as sql
from dataclasses import dataclass


con = sql.connect("database.db")
cur = con.cursor()

@dataclass
class User():
    username: str
    password: str


def login(username, password):
    ...


def signup(username, password):
    if check_username_available(username) == True:
        cur.execute("""INSERT INTO users VALUES
                        ('username'), ('password')
                        """)
        con.commit()
        con.close()
        return "Account Created"
    else:
        return "Account Creation Failed"


def check_username_available(username):
    if username == cur.execute("""SELECT username FROM users WHERE username='username'"""):
        return False
    else:
        return True


#def insertUser(username,password):
 #   con = sql.connect("database.db")
 #   cur = con.cursor()
 #   cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
 #   con.commit()
 #   con.close()

#def retrieveUsers():
	#con = sql.connect("database.db")
	#cur = con.cursor()
	#cur.execute("SELECT username, password FROM users")
	#users = cur.fetchall()
	#con.close()
	#return users

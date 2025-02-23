import sqlite3 as sql
from dataclasses import dataclass


con = sql.connect("database.db")
cur = con.cursor()


@dataclass
class User:
    username: str
    password: str


def login(username, password):
    pass


# Hint. Shouldnt this be in app.py? (then it can be a flask endpoint)
def signup(username: str, password: str) -> str:
    if check_username_available(username):
        insertUser(username, password)
        return "Account Created"
    else:
        return "Account Creation Failed"


def check_username_available(username):
    if username == cur.execute(
        """SELECT username FROM users WHERE username=(?)""", (username)
    ):
        return False
    else:
        return True


def insertUser(username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    # Hint. Use the above function
    cur.execute(
        "INSERT INTO users (username,password) VALUES (?,?)", (username, password)
    )
    con.commit()
    con.close()


def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    return users

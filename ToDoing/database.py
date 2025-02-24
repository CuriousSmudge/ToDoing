import sqlite3 as sql
from flask import g

db_file = "database.db"


def get_db() -> sql.Connection:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sql.connect(db_file)
    return db


def check_username_available(username):
    # con = get_db()
    # cur = con.cursor()
    cur = get_db().cursor()
    if username == cur.execute(
        """SELECT username FROM users WHERE username=?""",
        [username],
    ):
        return False
    else:
        return True


def insertUser(username, password):
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users  \
        (username,password) VALUES (?,?)",
        (username, password),
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

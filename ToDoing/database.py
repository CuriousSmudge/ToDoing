import sqlite3 as sql
from flask import g

db_file = "database.db"


def get_db() -> sql.Connection:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sql.connect(db_file)
    return db


def get_user(username) -> list:
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT username, password FROM users \
        WHERE (?) = username """,
        (username),
    )
    user = cur.fetchall()
    return user


def verify_username(username):
    user = get_user(username)
    if user[0] == username:
        return False
    else:
        return True


def insert_user(username, password):
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users  \
        (username,password) VALUES (?,?)",
        (username, password),
    )

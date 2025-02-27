import sqlite3 as sql
from flask import g
import auth
from auth import User

db_file = "database.db"


def get_db() -> sql.Connection:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sql.connect(db_file)
    return db


def get_user(username) -> User:
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT username, password, salt FROM users WHERE (?) = username """,
        (username,),
    )
    username, hashedPassword, salt = cur.fetchall()
    return User(username, hashedPassword, salt)


def does_user_exist(username) -> bool:
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT username FROM users WHERE (?) = username""",
        (username,),
    )
    if cur.fetchall() is None:
        return False
    elif username == cur.fetchall():
        return True


def insert_user(username, password):
    if does_user_exist(username):
        raise Exception
    encryption = auth.encrypt_password(password)
    hashedPassword = encryption[0]
    salt = encryption[1]

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users  \
        (username,password,salt) VALUES (?,?,?)",
        (username, hashedPassword, salt),
    )
    con.commit()

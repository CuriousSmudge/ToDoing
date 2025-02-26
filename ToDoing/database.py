import sqlite3 as sql
from flask import g
import auth
from auth import User
import main

db_file = "database.db"


def init():
    with main.app.app_context():
        con = get_db()
        cur = con.cursor()

        tables = cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table""")
        tables = [row[0] for row in cur.fetchall()]

        if "users" not in tables:
            cur.execute("""
                        CREATE TABLE users (
                        username NOT NULL,
                        password NOT NULL,
                        salt NOT NULL
                        )
                        """)
            con.commit()


init()


def get_db() -> sql.Connection:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sql.connect(db_file)
    return db


def get_user(username) -> User:
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT username, password, salt FROM users \
        WHERE (?) = username """,
        (username),
    )
    username, hashedPassword, salt = cur.fetchall()
    return User(username, hashedPassword, salt)


def insert_user(username, password):
    if auth.does_user_exist(username):
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

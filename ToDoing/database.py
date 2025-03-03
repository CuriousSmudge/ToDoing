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
        """SELECT username, password FROM users WHERE username = (?) """,
        (username,),
    )
    username, hashedPassword = cur.fetchone()
    return User(username, hashedPassword)


def does_user_exist(username) -> bool:
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT username FROM users WHERE (?) = username""",
        (username,),
    )
    result = cur.fetchone()
    if result is None:
        return False
    elif username == result:
        return True
    else:
        return False


def insert_user(username, password):
    if does_user_exist(username):
        raise Exception
    hashedPassword = auth.encrypt_password(password)

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users  \
        (username,password) VALUES (?,?)",
        (username, hashedPassword),
    )
    con.commit()


def get_tasks_for_user(username):
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT * FROM tasks WHERE (?) = username""",
        (username,),
    )
    data = cur.fetchall()

    result = []
    for task in data:
        dictionary = {}
        dictionary["id"] = task[0]
        dictionary["task"] = task[2]
        dictionary["completed"] = task[3]

        result.append(dictionary)

    return result


def add_task(username, task):
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO tasks \
            (username, task, completed) VALUES (?,?,0)""",
        (username, task),
    )
    con.commit()

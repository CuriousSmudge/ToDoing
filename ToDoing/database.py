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
    # Gets the user from the database based on username and returns User object
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT username, password FROM users WHERE username = (?) """,
        (username,),
    )

    d = cur.fetchone()
    username, hashedPassword = d
    return User(username, hashedPassword)


def does_user_exist(username) -> bool:
    # Checks the database for an existing user before insertion
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """SELECT username FROM users WHERE (?) = username""",
        (username,),
    )
    result = cur.fetchone()
    return username == result


def insert_user(username, password):
    # Inserts the user into the database while doing validation
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
    # Takes all of the users tasks from the database and sends them back
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
        dictionary["id"] = task[3]
        dictionary["task"] = task[1]
        dictionary["completed"] = task[2]

        result.append(dictionary)

    return result


def add_task(username, task):
    # Adds a new task entry for the user into the database
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """INSERT INTO tasks \
            (username, task, completed) VALUES (?,?,0)""",
        (username, task),
    )
    con.commit()


def toggle_completion(completion, identification):
    # Changes the completion level of the task
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """UPDATE tasks SET completed = (?) \
        WHERE id = (?)""",
        (completion, identification),
    )
    con.commit()


def remove_task_from_db(identification):
    # Removed task from database based on id of the task
    con = get_db()
    cur = con.cursor()
    cur.execute(
        """DELETE FROM tasks WHERE id = (?)""",
        (identification,),
    )
    con.commit()

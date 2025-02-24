from dataclasses import dataclass
from flask import request, session
import hashlib
import secrets
import functools
from main import app

import database


def require_api_token(func):
    @functools.wraps(func)
    def check_token(*args, **kwargs):
        if "api_session_token" not in session:
            return "Access denied"
        return func(*args, **kwargs)

    return check_token


@dataclass
class User:
    username: str
    password: str
    hashedPassword: bytes

    def hash_password(self, password) -> bytes:
        salt = secrets.token_bytes(64)
        t_sha = hashlib.sha256()
        t_sha.update(password + salt)
        hashedPassword = t_sha.digest()
        return hashedPassword

    def token(self): ...


@app.route("/signup", methods=["POST"])
def signup(username: str, password: str) -> str:
    username = request.form["username"]
    password = request.form["password"]
    if database.check_username_available(username):
        database.insertUser(username, password)
        return "Account Created"
    else:
        return "Account Creation Failed"

from dataclasses import dataclass
import hashlib
import secrets
from flask import request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from main import app
import database


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


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


@basic_auth.verify_password
def verify_password(username, password) -> User: ...


@app.route("/signup", methods=["POST"])
def signup(username: str, password: str) -> str:
    username = request.form["username"]
    password = request.form["password"]
    if database.check_username_available(username):
        database.insert_user(username, password)
        return "Account Created"
    else:
        return "Account Creation Failed"

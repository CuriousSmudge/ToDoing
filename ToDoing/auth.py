import hashlib
import secrets
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
import database


basic_auth = HTTPBasicAuth()


class User:
    username: str
    hashedPassword: bytes
    salt: bytes

    def __init__(self, username, hashedPassword, salt):
        self.username = username
        self.hashedPassword = hashedPassword
        self.salt = salt

    def __call__(self):
        return self.username, self.hashedPassword, self.salt


def encrypt_password(password) -> tuple:
    salt = secrets.token_bytes(32)
    password = bytes(password, "utf-8")
    t_sha = hashlib.sha256()
    t_sha.update(password + salt)
    hashedPassword = t_sha.digest()
    return hashedPassword, salt


@basic_auth.verify_password
def verify_password(username, password) -> User | None:
    database.get_user(username)
    if username in check_password_hash(username, password):
        return username

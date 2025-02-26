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


def does_user_exist(username) -> bool:
    user = database.get_user(username)
    if user()[0] == username:
        return True
    else:
        return False


def encrypt_password(password) -> tuple:
    salt = secrets.token_bytes(32)
    t_sha = hashlib.sha256()
    t_sha.update(password + salt)
    hashedPassword = t_sha.digest()
    return hashedPassword, salt


@basic_auth.verify_password
def verify_password(username, password) -> User | None:
    database.get_user(username)
    if username in check_password_hash(username, password):
        return username

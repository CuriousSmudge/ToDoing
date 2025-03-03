from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
import database


basic_auth = HTTPBasicAuth()


class User:
    username: str
    hashedPassword: str

    def __init__(self, username, hashedPassword):
        self.username = username
        self.hashedPassword = hashedPassword

    def __call__(self):
        return self.username, self.hashedPassword


def encrypt_password(password) -> str:
    hashedPassword = generate_password_hash(password)
    return hashedPassword


@basic_auth.verify_password
def verify_password(username, password) -> User | None:
    user = database.get_user(username)
    if check_password_hash(user.hashedPassword, password):
        return username


@basic_auth.error_handler
def basic_auth_error():
    return "ALKJSALKDJSDKLFJ"

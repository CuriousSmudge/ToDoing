from flask import Flask, render_template, send_file, request
import database

app = Flask(__name__, template_folder="templates")
import auth  # noqa:261

# -------------------------------------------------------------------------- #


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manifest.json")
def serve_manifest():
    return send_file("manifest.json", mimetype="application/manifest+json")


@app.route("/sw.js")
def serve_sw():
    return send_file("sw.js", mimetype="application/javascript")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login.css")
def serve_login_css():
    with open("static/login.css") as file:
        data = file.read()
    return data


@app.route("/signup")
def signup(username, password):
    username = request.form["username"]
    password = request.form["password"]
    database.insert_user(username, password)

from flask import Flask, render_template, send_file, request
import database

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manifest.json")
def serve_manifest():
    return send_file("manifest.json", mimetype="application/manifest+json")


@app.route("/sw.js")
def serve_sw():
    return send_file("sw.js", mimetype="application/javascript")


@app.route("/login.css")
def serve_login_css():
    # Hint. Use Send file here
    with open("static/login.css") as file:
        data = file.read()
    return data


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        signup(username, password)
        users = database.retrieveUsers()
        return render_template("login.html", users=users)
    else:
        return render_template("login.html")


@app.route("/signup", methods=["POST"])
def signup(username: str, password: str) -> str:
    username = request.form["username"]
    password = request.form["password"]
    if database.check_username_available(username):
        database.insertUser(username, password)
        return "Account Created"
    else:
        return "Account Creation Failed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

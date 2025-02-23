from flask import Flask, render_template, request, send_file
import database


database.login("baslls", "penis")

app = Flask(__name__, template_folder="templates")

# Hint. I would move signup and auth things to a new file


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manifest.json")
def serve_manifest():
    return send_file("manifest.json", mimetype="application/manifest+json")


@app.route("/sw.js")
def serve_sw():
    return send_file("sw.js", mimetype="application/javascript")


@app.route("/login", methods=["POST", "GET"])
def login():
    # hint. Have a seperate endpoint for sign up

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        database.signup(username, password)
        users = database.retrieveUsers()
        return render_template("login.html", users=users)
    else:
        return render_template("login.html")


@app.route("/login.css")
def serve_login_css():
    # Hint. Use Send file here

    with open("static/login.css") as file:
        data = file.read()
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

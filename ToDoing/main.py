from flask import Flask, render_template, send_file, request, jsonify

app = Flask(__name__, template_folder="templates")
import database  # noqa: E402
import auth  # noqa: E402

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


@app.route("/app")
def app_html():
    return render_template("app.html")


@app.route("/app.css")
def serve_app_css():
    with open("static/login.css") as file:
        data = file.read()
    return data


@app.post("/signup")
def signup():
    username = request.form["username"]
    password = request.form["password"]
    database.insert_user(username, password)
    return jsonify(1), 200


@app.get("/verify_user")
@auth.basic_auth.login_required
def verify_user():
    return jsonify(1), 200

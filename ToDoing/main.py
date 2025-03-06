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


@app.get("/tasks")
@auth.basic_auth.login_required
def get_tasks():
    # Gets the user's tasks from the database and return a list of them.
    username = auth.basic_auth.current_user()
    return database.get_tasks_for_user(username), 200


@app.post("/tasks")
@auth.basic_auth.login_required
def add_tasks():
    # Takes the username and task text and sends them to the database
    username = auth.basic_auth.current_user()
    task = request.form["task"]
    print(f"Task recived {task}")
    database.add_task(username, task)
    return jsonify(1), 200


@app.post("/task_status")
@auth.basic_auth.login_required
def change_task_status():
    # Sends the order to toggle the completion of the task based on what it is.
    print(request)
    identification = request.form["id"]
    completion = request.form["completion"]
    database.toggle_completion(completion, identification)
    return jsonify(1), 200


@app.post("/task_delete")
@auth.basic_auth.login_required
def delete_task():
    # Sends a request to the database to remove a task
    print(request)
    identification = request.form["id"]
    database.remove_task_from_db(identification)
    return jsonify(1), 200


@app.post("/signup")
def signup():
    # Assigns the username and password to the database
    username = request.form["username"]
    password = request.form["password"]
    database.insert_user(username, password)
    return jsonify(1), 200


@app.get("/verify_user")
@auth.basic_auth.login_required
def verify_user():
    # Uses basic auth and verify_password() function to check local credentials
    return jsonify(1), 200

import os
import json
from flask import (
    Flask, render_template, redirect, request, url_for, session, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


# Route for index
@app.route('/')
def index():
    data = []
    with open("data/projects.json", "r") as json_data:
        data = json.load(json_data)
    data_skill = []
    with open("data/skills.json", "r") as json_data:
        data_skill = json.load(json_data)
    return render_template("index.html", projects=data, skills=data_skill)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # if username not exists in db
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("portfolio", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session["user"]:
        # grab the session user's username from db
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        basic_info = mongo.db.basic_info.find()
        projects = mongo.db.projects.find()
        skills = mongo.db.skills.find()
        works = mongo.db.work_experience.find()
        return render_template(
            "profile.html", username=username,
            basic_info=basic_info, projects=projects,
            skills=skills, works=works)
    return redirect(url_for("login"))


@app.route("/portfolio/<username>", methods=["GET", "POST"])
def portfolio(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template("portfolio.html", username=username)
    return redirect(url_for("login"))


@app.route("/basic_info", methods=["GET", "POST"])
def basic_info():
    if request.method == "POST":
        basic = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "cur_title": request.form.get("cur_title"),
            "about_me": request.form.get("about_me"),
            "created_by": session["user"]
        }
        mongo.db.basic_info.insert_one(basic)
        flash(
            "Basic Information Successfully Added, Add Your Projects Info")
    return render_template("portfolio.html")


@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        project = {
            "project_name": request.form.get("project_name"),
            "project_desc": request.form.get("project_desc"),
            "project_link": request.form.get("project_link"),
            "created_by": session["user"]
        }
        mongo.db.projects.insert_one(project)
        flash(
            "Projects Information Successfully Added, Add more Projects Info")

    return render_template("portfolio.html")


@app.route("/work_experience", methods=["GET", "POST"])
def work_experience():
    if request.method == "POST":
        work_experience = {
            "job_title": request.form.get("job_title"),
            "company_name": request.form.get("company_name"),
            "from_date": request.form.get("from_date"),
            "to_date": request.form.get("to_date"),
            "created_by": session["user"]
        }
        mongo.db.work_experience.insert_one(work_experience)
        flash(
            "Experience Information Successfully Added, Add more Experience")

    return render_template("portfolio.html")


@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "POST":
        skills = {
            "skill_name": request.form.get("skill_name"),
            "percent": request.form.get("percent"),
            "created_by": session["user"]
        }
        mongo.db.skills.insert_one(skills)
        flash(
            "skills Information Successfully Added, Add more skills")

    return render_template("portfolio.html")


@app.route("/languages", methods=["GET", "POST"])
def languages():
    if request.method == "POST":
        languages = {
            "language_name": request.form.get("language_name"),
            "language_level": request.form.get("language_level"),
            "created_by": session["user"]
        }
        mongo.db.languages.insert_one(languages)
        flash(
            "Languages Information Successfully Added, Add more languages")

    return render_template("portfolio.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

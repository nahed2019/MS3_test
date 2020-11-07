import os
from flask import (
    Flask, render_template, redirect, request, url_for, session, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    """
    Render index template and find skills on MongoDB
    """
    skills = mongo.db.skills.find()
    projects = mongo.db.projects.find()
    project = mongo.db.projects.find_one()
    return render_template(
        'index.html', skills=skills, skill=skill,
        projects=projects, project=project)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

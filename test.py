@app.route("/add_profile/<username>", methods=["GET", "POST"])
def add_profile(username):
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
        return redirect(url_for("add_profile", username=username))

        project = {
            "project_name": request.form.get("project_name"),
            "project_desc": request.form.get("project_desc"),
            "project_link": request.form.get("project_link"),
            "created_by": session["user"]
        }
        mongo.db.projects.insert_one(project)
        flash(
            "Projects Information Successfully Added, Add Your Projects Info")
        return redirect(url_for("add_profile", username=username))

    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("add_profile.html", username=username)

    if session["user"]:
        return render_template("add_profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/basic_info", methods=["GET", "POST"])
def basic_info():
    if request.method == "POST":
        username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
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
        return redirect(url_for("add_profile", username=username))
    return render_template("basic_info.html")


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

    return render_template("add_project.html")

@app.route("/portfolio", methods=["GET", "POST"])
def portfolio():
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

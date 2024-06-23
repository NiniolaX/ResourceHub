#!/usr/bin/python3
""" ResourceHub Application Codebase """
from flask import abort, flash, Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from functools import wraps
import json
from models.learner import Learner
from models.school import School
from models.teacher import Teacher
from os import environ
from werkzeug.security import check_password_hash, generate_password_hash
import requests

app = Flask(__name__)
app.secret_key = 'my_secret_key'

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Function loads role user
@login_manager.user_loader
def load_user(user_id):
    response = requests.get(f"http://127.0.0.1:5001/api/users/{user_id}/")
    if response.status_code == 200:
        user_data = response.json()

        # Deserialize user dictionary by class
        if user_data['__class__'] == "School":
            return School(**user_data)
        elif user_data['__class__'] == "Teacher":
            return Teacher(**user_data)
        else:
            return Learner(**user_data)

    return None

# Function handles role based access control 
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not isinstance(current_user, role):
                abort(403) # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/")
def home():
    """ Returns the homepage """
    return render_template("home.html")


@app.route("/signup", strict_slashes=False)
def signup():
    """Returns the signup page"""
    return render_template("signup.html")


@app.route("/signup", methods=['POST'], strict_slashes=False)
def signup_post():
    """ Handles user registration """
    # Extract school information from form data
    school_info = {
                   "name": request.form["name"],
                   "email": request.form["email"],
                   "password": generate_password_hash(request.form["password"])
                  }

    response = requests.post("http://127.0.0.1:5001/api/schools/",
                             data=json.dumps(school_info),
                             headers={"Content-Type": "application/json"})

    # Check if error occured with school creation
    if response.status_code != 201:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
        return redirect(url_for("signup"))

    # Redirect client to login
    flash("School created successfully!", "success")
    return redirect(url_for("login"))


@app.route("/login", strict_slashes=False)
def login():
    """ Returns the login page """
    return render_template("login.html")


@app.route("/login", methods=['POST'], strict_slashes=False)
def login_post():
    """ Authenticates a user """
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']

    # Check that user exists
    response = requests.get(f"http://127.0.0.1:5001/api/usersbyemail/{email}/")
    if response.status_code == 404:
        flash("User does not exist")
        return redirect(url_for('signup'))

    # Check that user password is correct
    user_data = response.json()
    if check_password_hash(user_data['password'], password):
        user = School(**user_data)
        login_user(user)
        return redirect(url_for('render_dashboard'))
    else:
        flash("Incorrect password, try again.")
        return redirect(url_for('login'))


@app.route("/dashboard", strict_slashes=False)
@login_required
def render_dashboard():
    """ Returns the school dashboard """
    if isinstance(current_user, School):
        return render_template("school_dashboard.html", name=current_user.name)
    elif isinstance(current_user, Teacher):
        return render_template("teacher_dashboard.html", name=current_user.fname)
    else:
        return render_template("learner_dashboard.html", name=current_user.fname)


@app.route("/logout", methods=["GET", "POST"], strict_slashes=False)
@login_required
def logout():
    """ Logs out a user """
    logout_user()
    return redirect(url_for('login'))


@app.route("/manage-departments", strict_slashes=False)
@login_required
@role_required(Teacher)
def render_manage_departments():
    """ Renders manage departments page """
    return render_template("manage_departments.html")

#@app.route("/dashboard/manage-teachers")
#@app.route("/dashboard/manage-learners")
#@app.route("/dashboard/create-resource")
#@app.route("/dashboard/view-resources")

if __name__ == "__main__":
    """ Start the Flask application """
    app.run(host='0.0.0.0', port=5000, debug=True)

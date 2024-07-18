#!/usr/bin/python3
""" ResourceHub Application Codebase """
from app.generic_user_model import GenericUser
from flask import abort, flash, Flask, redirect, render_template, request, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from functools import wraps
from os import environ
from werkzeug.security import check_password_hash, generate_password_hash
import json
import requests

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY', 'default_secret_key')

# Define conditions for Cross-Origin Resource Sharing
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Get API URL 
api_url = environ.get('API_URL')

# Function to load user into login manager
@login_manager.user_loader
def load_user(user_id):
    response = requests.get(f"{api_url}/users/{user_id}/")
    if response.status_code == 200:
        user_data = response.json()
        # Rebuild user from its dict representation
        return GenericUser(**user_data)

    return None

# Function to handle role based access control 
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
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
    return render_template("sign_up.html")

@app.route("/about", strict_slashes=False)
def about():
    """ Returns the about us page """
    return render_template("about_us.html")

@app.route("/signup", methods=['POST'], strict_slashes=False)
def signup_post():
    """ Handles school registration """
    # Extract school information from form data
    school_info = {
                   "name": request.form["name"],
                   "email": request.form["email"],
                   "password": generate_password_hash(request.form["password"])
                  }

    response = requests.post(f"{api_url}/schools/",
                             data=json.dumps(school_info),
                             headers={"Content-Type": "application/json"})

    # Check if error occured with school creation
    if response.status_code != 201:
        error_message = response.json().get("error", "An error has occured") # Extracts error message returned by API
        flash(error_message)
        return redirect(url_for("signup"))

    # Redirect client to login
    flash("School created successfully! Login here.", "success")
    return redirect(url_for("login"))


@app.route("/login", strict_slashes=False)
def login():
    """ Returns the login page """
    return render_template("log_in.html")


@app.route("/login", methods=['POST'], strict_slashes=False)
def login_post():
    """ Authenticates a user """
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']

    # Check that user exists
    response = requests.get(f"{api_url}/usersbyemail/{email}/")
    if response.status_code == 404:
        flash("User does not exist", "error")
        return redirect(url_for('login'))

    # Check that user's password is correct
    user_data = response.json()
    if check_password_hash(user_data['password'], password):
        user = GenericUser(**user_data)
        # Check that user selected appropriate user type
        if user.role != user_type:
            flash("Incorrect user type.", "error")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('render_dashboard'))
    else:
        flash("Incorrect password, try again.", "error")
        return redirect(url_for('login'))


@app.route("/dashboard", strict_slashes=False)
@login_required
def render_dashboard():
    """ Renders the appropriate dashboard """
    if current_user.role == "School":
        return render_template("school_dashboard.html")

    elif current_user.role == "Teacher":
        teacher_id = current_user.id
        response = requests.get(f"{api_url}/teachers/{teacher_id}/resources")
        if response.status_code == 200:
            try:
                resources = response.json()
            except requests.exceptions.JSONDecodeError:
                flash("Error decoding resources data", "error")
                resources = []
        else:
            flash("Failed to fetch resources", "error")
            resources = []
        return render_template("teacher_dashboard.html", resources=resources)

    elif current_user.role == "Learner":
        department_id = current_user.department_id
        response = requests.get(f"{api_url}/departments/{department_id}/resources")
        if response.status_code == 200:
            try:
                resources = response.json()
            except requests.exceptions.JSONDecodeError:
                flash("Error decoding resources data", "error")
                resources = []
        else:
            flash("Failed to fetch resources", "error")
            resources = []
        return render_template("learner_dashboard.html", resources=resources)

    else:
        flash('Not a valid user type', 'error')
        return redirect(url_for('login'))


@app.route("/logout", methods=["GET", "POST"], strict_slashes=False)
@login_required
def logout():
    """ Logs out a user """
    logout_user()
    return redirect(url_for('login'))


@app.route("/manage-departments", strict_slashes=False)
@login_required
@role_required('School')
def render_manage_departments():
    """ Renders manage departments page """
    school_id = current_user.id
    response = requests.get(f"{api_url}/schools/{school_id}/departments")
    departments = response.json()
    return render_template("manage_departments.html",
                           departments=departments)


@app.route("/add-department", methods=["POST"], strict_slashes=False)
@login_required
@role_required('School')
def add_department():
    """ Adds a new department to a school """
    name = request.form["name"]
    school_id = current_user.id
    response = requests.post(f"{api_url}/schools/{school_id}/departments",
                             data=json.dumps({"name": name}),
                             headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        flash("Department added successfully!", "success")
    else:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    return redirect(url_for("render_manage_departments"))


@app.route("/delete-department", methods=["POST"], strict_slashes=False)
@login_required
@role_required('School')
def delete_department():
    """ Deletes a department """
    department_id = request.form["department_id"]
    response = requests.delete(f"{api_url}/departments/{department_id}")
    if response.status_code != 200:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    else:
        flash("Department deleted successfully!", "success")
    return redirect(url_for("render_manage_departments"))


@app.route("/manage-teachers", strict_slashes=False)
@login_required
@role_required('School')
def render_manage_teachers():
    """ Renders manage teachers page """
    school_id = current_user.id

    # Get departments
    response = requests.get(f"{api_url}/schools/{school_id}/departments")
    departments = response.json()

    # Get teachers
    teachers = {}
    for department in departments:
        department_id = department['id']
        response2 = requests.get(f"{api_url}/departments/{department_id}/teachers")
        teachers[department_id] = response2.json()

    return render_template("manage_teachers.html", departments=departments, teachers=teachers)


@app.route("/add-teacher", methods=["POST"], strict_slashes=False)
@login_required
@role_required('School')
def add_teacher():
    """ Adds a new teacher to a school """
    teacher_info = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "title": request.form.get("title"),
        "password": generate_password_hash(request.form["lname"].lower())
    }
    department_id = request.form["department_id"]
    response = requests.post(f"{api_url}/departments/{department_id}/teachers",
                             data=json.dumps(teacher_info),
                             headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        flash("Teacher added successfully!", "success")
    else:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    return redirect(url_for("render_manage_teachers"))


@app.route("/delete-teacher", methods=["POST"], strict_slashes=False)
@login_required
@role_required('School')
def delete_teacher():
    """ Deletes a teacher from a school """
    teacher_id = request.form["teacher_id"]
    response = requests.delete(f"{api_url}/teachers/{teacher_id}")
    if response.status_code != 200:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    else:
        flash("Teacher deleted successfully!", "success")
    return redirect(url_for("render_manage_teachers"))


@app.route("/manage-learners", strict_slashes=False)
@login_required
@role_required('School')
def render_manage_learners():
    """ Renders manage learners page """
    school_id = current_user.id

    # Get departments
    response = requests.get(f"{api_url}/schools/{school_id}/departments")
    departments = response.json()

    # Get teachers
    learners = {}
    for department in departments:
        department_id = department['id']
        response2 = requests.get(f"{api_url}/departments/{department_id}/learners")
        learners[department_id] = response2.json()

    return render_template("manage_learners.html", departments=departments, learners=learners)


@app.route("/add-learner", methods=["POST"], strict_slashes=False)
@login_required
@role_required('School')
def add_learner():
    """ Adds a new learner to a school """
    learner_info = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "password": generate_password_hash(request.form["lname"].lower())
    }
    department_id = request.form["department_id"]
    response = requests.post(f"{api_url}/departments/{department_id}/learners",
                             data=json.dumps(learner_info),
                             headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        flash("Learner added successfully!", "success")
    else:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    return redirect(url_for("render_manage_learners"))


@app.route("/delete-learner", methods=["POST"], strict_slashes=False)
@login_required
@role_required('School')
def delete_learner():
    """ Deletes a learner from a school """
    learner_id = request.form["learner_id"]
    response = requests.delete(f"{api_url}/learners/{learner_id}")
    if response.status_code != 200:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    else:
        flash("Learner deleted successfully!", "success")
    return redirect(url_for("render_manage_learners"))


@app.route("/create-resource", strict_slashes=False)
@login_required
@role_required('Teacher')
def render_create_resource():
    """ Returns the create resource page """
    return render_template("create_resource.html")


@app.route("/create-resource", methods=["POST"], strict_slashes=False)
@login_required
@role_required('Teacher')
def create_resource():
    """ Creates a resource """
    resource_info = {
        "title": request.form['title'],
        "content": request.form['content']
    }
    teacher_id = request.form['teacher_id']
    response = requests.post(f"{api_url}/teachers/{teacher_id}/resources",
                             data=json.dumps(resource_info),
                             headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        flash("New resource created!", "success")
    else:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    return redirect(url_for("render_dashboard"))
    

@app.route("/delete-resource", methods=["POST"], strict_slashes=False)
@login_required
@role_required('Teacher')
def delete_resource():
    """ Deletes a resource """
    resource_id = request.form["resource_id"]
    response = requests.delete(f"{api_url}/resources/{resource_id}")
    if response.status_code != 200:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)
    else:
        flash("Resource deleted successfully!", "success")
    return redirect(url_for("render_dashboard"))


@app.route("/resources/<slug>", strict_slashes=False)
@login_required
def view_resource(slug):
    """ Views a resource by slug """
    response = requests.get(f"{api_url}/resourcesbyslug/{slug}")
    if response.status_code == 200:
        resource = response.json()

        # Remove time from resource creation date
        t_index = resource['created_at'].find('T')
        resource['created_at'] = resource['created_at'][:t_index]
        return render_template('view_resource.html', resource=resource)
    else:
        error_message = response.json().get("error", "An error has occured")
        flash(error_message)


if __name__ == "__main__":
    """ Start the Flask application """
    host = environ.get('APP_HOST', '0.0.0.0')
    port = int(environ.get('APP_PORT', 5000))
    app.run(host=host, port=port, debug=True)

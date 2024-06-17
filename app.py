#!/usr/bin/python3
""" ResourceHub Application Codebase """
from flask import Flask, render_template
from os import environ
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route("/", methods=[GET])
def home():
    """ Returns the homepage """
    return render_template("home.html")

@app.route("/signup", methods=[GET], strict_slashes=False)
def signup_page():
    """Returns the signup page"""
    return render_template("signup.html")

@app.route("/signup", methods=[POST], strict_slashes=False)
def signup():
    """ Handles user registration """

@qpp.route("/dashboard")
@app.route("/dashboard/manage-departments")
@app.route("/dashboard/manage-teachers")
@app.route("/dashboard/manage-learners")
@app.route("/dashboard/create-resource")
@app.route("/dashboard/view-resources")

if __name__ == "__main__":
    """ Start the Flask application """
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

api_views = Blueprint('api_views', __name__, url_prefix="/api")

# Import views
from api.views.schools import *
from api.views.departments import *
from api.views.teachers import *
from api.views.learners import *
from api.views.resources import *
from api.views.users import *

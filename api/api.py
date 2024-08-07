#!/usr/bin/python3
""" Application API

Attributes:
    api: An instance of the Flask class, which is the application object

    Functions:
        teardown_db: Cleans up after each call to API
        return_404: Handles the 404 error

    Classes:
        None
"""
from api.models import storage
from api.views import api_views
from flask import Flask, make_response, jsonify, redirect
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from os import environ

api = Flask(__name__)
api.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# Register Blueprint
api.register_blueprint(api_views)

# Define conditions for Cross-Origin Resource Sharing
cors = CORS(api, resources={r"/api/*": {"origins": "*"}})


@api.teardown_appcontext
def close_db(error):
    """ Close database session """
    storage.close()


@api.errorhandler(404)
def not_found(error):
    """ Raise 404 error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@api.errorhandler(500)
def server_error(error):
    """ Raise 500 error
    ---
    responses:
      500:
        description: an internal server error occured
    """
    return make_response(jsonify({"error": "Internal server error"}), 500)


api.config['SWAGGER'] = {
    'title': 'ResourceHub Restful API',
    'uiversion': 3
}
Swagger(api)


if __name__ == "__main__":
    """ Main Function """
    host = "0.0.0.0"
    port = int(environ.get("PORT", 5001))
    api.run(host=host, port=port, threaded=True, debug=True)

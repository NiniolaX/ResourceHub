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
from api.views import api_views
from flask import Flask, make_response, jsonify
# from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from models import storage
from os import environ

api = Flask(__name__)
api.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# Register Blueprint
api.register_blueprint(api_views)

# Define conditions for Cross-Origin Resource Sharing
# cors = CORS(api, resources={r"/api/*": {"origins": "*"}})


@api.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@api.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({"error": "Not found"}), 404)


api.config["SWAGGER"] = {
    "title": "ResourceHub RESTful API",
    "uiversion": 3
}

Swagger(api)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(environ.get("HBNB_API_PORT", 5001))
    api.run(host=host, port=port, threaded=True, debug=True)

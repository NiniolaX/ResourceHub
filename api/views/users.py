#!/usr/bin/python3
""" Handles all default RestFul API actions for Users """
from api.models import storage
from api.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('api/views/documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves a specific user by id """
    users = storage.all().values()
    for item in users:
        if item.id == user_id:
            user = item
            return jsonify(user.to_dict())

    abort(404)

@api_views.route('/usersbyemail/<email>', methods=['GET'], strict_slashes=False)
@swag_from('api/views/documentation/user/get_user_by_email.yml', methods=['GET'])
def get_user_by_email(email):
    """ Retrieves a specific user by email """
    user = storage.get_user_by_email(email)
    if not user:
        abort(404)

    return jsonify(user.to_dict())

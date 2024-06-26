#!/usr/bin/python3
""" Handles all default RestFul API actions for Learners """
from api.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models import storage
from models.department import Department
from models.learner import Learner
from models.school import School


@api_views.route('/departments/<department_id>/learners',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/learner/get_learner.yml', methods=['GET'])
def get_learners(department_id):
    """
    Retrieves the list of learners in a department from database
    """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)
    learner_list = [learner.to_dict()
                    for learner in department.learners]

    return jsonify(learner_list)


@api_views.route('/departments/<department_id>/learners',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/learner/post_learner.yml', methods=['POST'])
def create_learner(department_id):
    """
    Adds a new learner to database
    """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    # Check that serializable data was passed
    try:
        request_data = request.get_json()
    except Exception as e:
        return make_response({"error": "Not a JSON"}, 400)

    # Check that required parameters were passed
    required_params = ["fname", "lname", "email", "password"]
    for param in required_params:
        if param not in request_data:
            return make_response({"error": f"Missing {param}"}, 400)

    # Check that email does not already exist
    if not storage.is_email_unique(request_data['email']):
        return make_response({"error": "Email already exists"}, 400)

    # Build data to pass to model for object creation
    data = {
            "department_id": department_id,
            "school_id": department.school_id,
            "fname": request_data['fname'],
            "lname": request_data['lname'],
            "email": request_data['email'],
            "password": request_data['password']
    }

    new_learner = Learner(**data)
    new_learner.save()

    return jsonify(new_learner.to_dict()), 201


@api_views.route('/learners/<email>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/learner/get_email_learner.yml', methods=['get'])
def get_learner(email):
    """ Retrieves a learner from database """
    learner = storage.get_user_by_email(email, "learner")
    if not learner:
        abort(404)

    return jsonify(learner.to_dict())


@api_views.route('/learners/<learner_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/learner/delete_learner.yml', methods=['DELETE'])
def delete_learner(learner_id):
    """ Deletes a learner from database """

    learner = storage.get(Learner, learner_id)
    if not learner:
        abort(404)

    storage.delete(learner)

    return jsonify({}), 200


@api_views.route('/learners/<learner_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/learner/put_learner.yml', methods=['PUT'])
def update_learner(learner_id):
    """ Updates a learner in databse """
    learner = storage.get(Learner, learner_id)
    if not learner:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore = ['id', 'created_at', 'updated_at']

    request_data = request.get_json()
    for key, value in request_data.items():
        if key not in ignore:
            setattr(learner, key, value)
    storage.save()

    return jsonify(learner.to_dict()), 200

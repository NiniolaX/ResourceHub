#!/usr/bin/python3
""" Handles all default RestFul API actions for Schools """
from api.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models import storage
from models.school import School


@api_views.route('/schools', methods=['GET'], strict_slashes=False)
@swag_from('documentation/school/get_school.yml', methods=['GET'])
def get_schools():
    """
    Retrieves the list of schools in database
    """
    schools = storage.all(School).values()
    schools_list = [school.to_dict() for school in schools]
    return jsonify(schools_list)


@api_views.route('/schools', methods=['POST'], strict_slashes=False)
@swag_from('documentation/school/post_school.yml', methods=['POST'])
def create_school():
    """
    Creates a new school
    """
    try:
        request_data = request.get_json()
    except Exception as e:
        return make_response({"error": "Not a JSON"}, 400)

    # Check that required parameters were passed
    required_params = ["name", "email", "password"]
    for param in required_params:
        if param not in request_data:
            return make_response({"error": f"Missing {param}"}, 400)

    # Check if school name exists (Used set for quicker membership tests)
    schools = storage.all(School).values()
    school_names = {school.name for school in schools}
    if request_data['name'] in school_names:
        return make_response({"error": "School already exists"}, 400)

    # Check that email does not exist
    if not storage.is_email_unique(request_data['email']):
        return make_response({"error": "Email already exists"}, 400)

    new_school = School(**request_data)
    new_school.save()

    return jsonify(new_school.to_dict()), 201


@api_views.route('/schools/<email>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/school/get_email_school.yml', methods=['get'])
def get_school(email):
    """ Retrieves a specific School """
    school = storage.get_user_by_email(email, "school")
    if not school:
        abort(404)

    return jsonify(school.to_dict())


@api_views.route('/schools/<school_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/school/delete_school.yml', methods=['DELETE'])
def delete_school(school_id):
    """
    Deletes a School Object
    """

    school = storage.get(School, school_id)
    if not school:
        abort(404)

    storage.delete(school)

    return jsonify({}), 200


@api_views.route('/schools/<school_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/school/put_school.yml', methods=['PUT'])
def update_school(school_id):
    """
    Updates a School
    """
    school = storage.get(School, school_id)
    if not school:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore = ['id', 'created_at', 'updated_at']

    request_data = request.get_json()
    for key, value in request_data.items():
        if key not in ignore:
            setattr(school, key, value)
    storage.save()

    return jsonify(school.to_dict()), 200

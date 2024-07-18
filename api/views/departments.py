#!/usr/bin/python3
""" Handles all default RestFul API actions for Departments """
from api.models import storage
from api.models.department import Department
from api.models.school import School
from api.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route('/schools/<school_id>/departments', methods=['GET'], strict_slashes=False)
@swag_from('documentation/department/get_departments.yml', methods=['GET'])
def get_departments(school_id):
    """
    Retrieves list of departments in a school from database.
    """
    school = storage.get(School, school_id)
    if not school:
        abort(404)

    department_list = [department.to_dict()
                       for department in school.departments]

    return jsonify(department_list)


@api_views.route('/schools/<school_id>/departments', methods=['POST'], strict_slashes=False)
@swag_from('documentation/department/post_department.yml', methods=['POST'])
def create_department(school_id):
    """
    Adds a new department to a school in database.
    """
    school = storage.get(School, school_id)
    if not school:
        abort(404)

    try:
        request_data = request.get_json()
    except Exception as e:
        return make_response({"error": "Not a JSON"}, 400)

    # Check that required parameters were passed
    required_params = ["name"]
    for param in required_params:
        if param not in request_data:
            return make_response({"error": f"Missing {param}"}, 400)

    # Check that department name does not already exist in database
    for department in school.departments:
        if department.name == request_data['name']:
            return make_response({"error": "Department already exists"}, 400)

    # Build data to pass to model for object creation
    data = {
            "school_id": school_id,
            "name": request_data['name']
    }

    new_department = Department(**data)
    new_department.save()

    return jsonify(new_department.to_dict()), 201


@api_views.route('/departments/<department_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/department/get_department.yml', methods=['GET'])
def get_department(department_id):
    """ Retrieves a specific department of a school from database.
    """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    return jsonify(department.to_dict())


@api_views.route('/departments/<department_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/department/delete_department.yml', methods=['DELETE'])
def delete_department(department_id):
    """
    Deletes a department from school in database.
    """

    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    storage.delete(department)

    return jsonify({}), 200


@api_views.route('/departments/<department_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/department/put_department.yml', methods=['PUT'])
def update_department(department_id):
    """
    Updates a department of a school in database.
    """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore = ['id', 'created_at', 'updated_at']

    request_data = request.get_json()
    for key, value in request_data.items():
        if key not in ignore:
            setattr(department, key, value)
    storage.save()

    return jsonify(department.to_dict()), 200

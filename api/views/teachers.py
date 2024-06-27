#!/usr/bin/python3
""" Handles all default RestFul API actions for Teachers """
from api.models import storage
from api.models.department import Department
from api.models.school import School
from api.models.teacher import Teacher
from api.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route('/departments/<department_id>/teachers',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/teacher/get_teacher.yml', methods=['GET'])
def get_teachers(department_id):
    """
    Retrieves the list of teachers in a department from database
    """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)
    teacher_list = [teacher.to_dict()
                    for teacher in department.teachers]

    return jsonify(teacher_list)


@api_views.route('/departments/<department_id>/teachers',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/teacher/post_teacher.yml', methods=['POST'])
def create_teacher(department_id):
    """
    Adds a new teacher to database
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
            "title": request_data.get('title'),
            "fname": request_data['fname'],
            "lname": request_data['lname'],
            "email": request_data['email'],
            "password": request_data['password']
    }

    new_teacher = Teacher(**data)
    new_teacher.save()

    return jsonify(new_teacher.to_dict()), 201


@api_views.route('/teachers/<teacher_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/teacher/get_id_teacher.yml', methods=['get'])
def get_teacher(teacher_id):
    """ Retrieves a specific Teacher """
    teacher = storage.get(Teacher, teacher_id)
    if not teacher:
        abort(404)

    return jsonify(teacher.to_dict())


@api_views.route('/teachers/<teacher_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/teacher/delete_teacher.yml', methods=['DELETE'])
def delete_teacher(teacher_id):
    """
    Deletes a Teacher Object
    """

    teacher = storage.get(Teacher, teacher_id)
    if not teacher:
        abort(404)

    storage.delete(teacher)

    return jsonify({}), 200


@api_views.route('/teachers/<teacher_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/teacher/put_teacher.yml', methods=['PUT'])
def update_teacher(teacher_id):
    """
    Updates a Teacher
    """
    teacher = storage.get(Teacher, teacher_id)
    if not teacher:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore = ['id', 'created_at', 'updated_at']

    request_data = request.get_json()
    for key, value in request_data.items():
        if key not in ignore:
            setattr(teacher, key, value)
    storage.save()

    return jsonify(teacher.to_dict()), 200

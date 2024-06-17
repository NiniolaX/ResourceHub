#!/usr/bin/python3
""" Handles all default RestFul API actions for Resources """
from api.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models import storage
from models.department import Department
from models.resource import Resource
from models.teacher import Teacher


@api_views.route('/departments/<department_id>/resources',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_resource.yml', methods=['GET'])
def get_resources(department_id):
    """
    Retrieves the list of resources in a department from database
    """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)
    resource_list = [resource.to_dict()
                    for resource in department.resources]

    return jsonify(resource_list)


@api_views.route('/teachers/<teacher_id>/resources',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/resource/post_resource.yml', methods=['POST'])
def create_resource(teacher_id):
    """
    Adds a new resource to database
    """
    teacher = storage.get(Teacher, teacher_id)
    if not teacher:
        abort(404)

    # Check that serializable data was passed
    try:
        request_data = request.get_json()
    except Exception as e:
        return make_response({"error": "Not a JSON"}, 400)

    # Check that required parameters were passed
    required_params = ["title", "content"]
    for param in required_params:
        if param not in request_data:
            return make_response({"error": f"Missing {param}"}, 400)

    # Build data to pass to model for object creation
    data = {
            "department_id": teacher.department_id,
            "school_id": teacher.school_id,
            "teacher_id": teacher_id,
            "title": request_data['title'],
            "description": request_data.get("description"),
            "content": request_data['content']
    }

    new_resource = Resource(**data)
    new_resource.save()

    return jsonify(new_resource.to_dict()), 201


@api_views.route('/resources/<resource_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_id_resource.yml', methods=['get'])
def get_resource(resource_id):
    """ Retrieves a specific Resource """
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404)

    return jsonify(resource.to_dict())


@api_views.route('/resources/<resource_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/resource/delete_resource.yml', methods=['DELETE'])
def delete_resource(resource_id):
    """
    Deletes a Resource Object
    """

    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404)

    storage.delete(resource)

    return jsonify({}), 200


@api_views.route('/resources/<resource_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/resource/put_resource.yml', methods=['PUT'])
def update_resource(resource_id):
    """
    Updates a Resource
    """
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore = ['id', 'created_at', 'updated_at']

    request_data = request.get_json()
    for key, value in request_data.items():
        if key not in ignore:
            setattr(resource, key, value)
    storage.save()

    return jsonify(resource.to_dict()), 200

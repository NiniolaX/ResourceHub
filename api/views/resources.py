#!/usr/bin/python3
""" Handles all default RestFul API actions for Resources """
from api.models import storage
from api.models.department import Department
from api.models.resource import Resource
from api.models.teacher import Teacher
from api.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
import uuid


@api_views.route('/departments/<department_id>/resources', methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_resources_by_dept.yml', methods=['GET'])
def get_resources_by_department(department_id):
    """
    Retrieves the list of resources in a department from database
    """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    resource_list = []
    for resource in department.resources:
        resource_dict = resource.to_dict()
        # Serialize teacher object in resource as well
        teacher = resource.teacher
        if teacher:
            resource_dict['teacher'] = teacher.to_dict()
            # Delete password of teacher from resource dict to be returned
            del resource_dict['teacher']['password']
        resource_list.append(resource_dict)

    return jsonify(resource_list)


@api_views.route('/teachers/<teacher_id>/resources', methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_resources_by_teacher.yml', methods=['GET'])
def get_resources_by_teacher(teacher_id):
    """
    Retrieves all resources by a specific teacher
    """
    teacher = storage.get(Teacher, teacher_id)
    if not teacher:
        abort(404)

    resource_list = [resource.to_dict() for resource in teacher.resources]

    return jsonify(resource_list)


@api_views.route('/teachers/<teacher_id>/resources', methods=['POST'], strict_slashes=False)
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
    slug = generate_unique_slug(request_data['title'])
    data = {
            "teacher_id": teacher_id,
            "department_id": teacher.department_id,
            "school_id": teacher.school_id,
            "title": request_data['title'],
            "slug": slug,
            "content": request_data['content']
    }

    new_resource = Resource(**data)
    new_resource.save()

    return jsonify(new_resource.to_dict()), 201


def generate_unique_slug(title):
    """ Generates a unique slug for an article """
    slug = title.lower().replace(' ', '-')
    unique_slug = f"{slug}-{str(uuid.uuid4())}"
    return unique_slug


@api_views.route('/resources/<resource_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_resource.yml', methods=['GET'])
def get_resource(resource_id):
    """ Retrieves a specific Resource """
    resource = storage.get(Resource, resource_id)
    if not resource:
        abort(404)

    resource_dict = resource.to_dict()
    # Serialize teacher object in resource as well
    teacher = resource.teacher
    if teacher:
        resource_dict['teacher'] = teacher.to_dict()
        del resource_dict['teacher']['password']

    return jsonify(resource_dict)


@api_views.route('/resourcesbyslug/<slug>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/resource/get_resource_by_slug.yml', methods=['GET'])
def get_resource_by_slug(slug):
    """ Retrieves a specific Resource """
    for resource in storage.all(Resource).values():
        if resource.slug == slug:
            # Searialize teacher object in resource
            resource_dict = resource.to_dict()
            teacher = resource.teacher
            if teacher:
                resource_dict['teacher'] = teacher.to_dict()
                del resource_dict['teacher']['password']
            return jsonify(resource_dict)

    abort(404)


@api_views.route('/resources/<resource_id>', methods=['DELETE'], strict_slashes=False)
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

#!/usr/bin/python3
""" Tests the resource view of the API """
import unittest
import json
from api.api import api
from models import storage
from models.department import Department
from models.learner import Learner
from models.resource import Resource
from models.school import School
from models.teacher import Teacher
from os import getenv


class ResourceApiTestCase(unittest.TestCase):
    """ Tests the resources view of the API """
    def setUp(self):
        """ Sets up test environment """
        self.api = api.test_client()
        self.api.testing = True

        # Create application context
        self.api_context = api.app_context()
        self.api_context.push()

        # Initialize storage
        storage.reload()

        # Create test objects
        self.school = School(name="Test School",
                             email="test@gmail.com",
                             password="123")
        self.department = Department(name="Test Department",
                                     school_id=self.school.id)
        self.teacher = Teacher(fname="Test",
                               lname="Teacher",
                               email="test01@gmail.com",
                               password="123",
                               department_id=self.department.id,
                               school_id=self.school.id)
        self.resource = Resource(title="The Art of War",
                                 slug="the-art-of-war-abcde-23453-86987",
                                 content="""
                                            1. Sun Tzu said: The art of war is
                                            of vital importance to the State.
                                            2. It is a matter of life and death,
                                            a road either to safety or to ruin.
                                            Hence it is a subject of inquiry
                                            which can on no account be neglected.
                                            3. The art of war, then, is governed
                                            by five constant factors, to be
                                            taken into account in one’s deliberations,
                                            when seeking to determine the conditions
                                            obtaining in the field.
                                            4. These are:
                                                (1) The Moral Law;
                                                (2) Heaven;
                                                (3) Earth;
                                                (4) The Commander;
                                                (5) Method and discipline
                                            """,
                                teacher_id=self.teacher.id,
                                department_id=self.department.id,
                                school_id=self.school.id)
        self.school.save()
        self.department.save()
        self.teacher.save()
        self.resource.save()

    def tearDown(self):
        """ Cleans up test environment """
        self.resource.delete()
        self.teacher.delete()
        self.department.delete()
        self.school.delete()
        storage.close()
        self.api_context.pop()

    def test_resources_created(self):
        """Check that test objects exist in storage"""
        self.assertIn(self.school, storage.all(School).values())
        self.assertIn(self.department, storage.all(Department).values())
        self.assertIn(self.teacher, storage.all(Teacher).values())
        self.assertIn(self.resource, storage.all(Resource).values())

    def test_get_resources(self):
        """ Test GET /api/departments/<department_id>/resources endpoint """
        response = self.api.get(f"/api/departments/{self.department.id}/resources/")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        # Check that resource object exists in data returned
        self.assertIn(self.resource.to_dict(), data_returned)
        # Check that object of different class does not exist in data returned
        other_classes = ["School", "Department", "Teacher", "Learner"]
        for obj in data_returned:
            self.assertTrue(obj["__class__"] not in other_classes)

    def test_get_resource(self):
        """ Test GET /api/resources/<resource_id> endpoint """
        response = self.api.get(f"/api/resources/{self.resource.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, self.resource.to_dict())

    def test_delete_resource(self):
        """ Test DELETE /api/resources/<resource_id> endpoint """
        response = self.api.delete(f"/api/resources/{self.resource.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_resource(self):
        """ Test POST /api/teachers/<teacher_id>/resources/ endpoint """
        # Create new resource via API
        new_resource_info = {"title": "The 48 Laws of Power",
                             "slug": "the-48-laws-of-power-0876-cdrfgv3",
                             "content": """
                                        48 Laws of Power details the laws
                                        for attaining power in life, business,
                                        and more.
                                        """,
                             "teacher_id": self.teacher.id,
                             "department_id": self.department.id,
                             "school_id": self.school.id}
        create_response = self.api.post(f"/api/teachers/{self.teacher.id}/resources/",
                                        data=json.dumps(new_resource_info),
                                        content_type="application/json")
        # Check response of API query
        self.assertEqual(create_response.status_code, 201)
        data_returned = json.loads(create_response.data)
        self.assertIn("id", data_returned)
        self.assertEqual(data_returned["title"], "The 48 Laws of Power")

        # Check that new object is in storage
        resource_id = data_returned["id"]
        self.assertIn(f'Resource.{resource_id}', storage.all(Resource))

        # Delete new resource via api (no duplicate resources allowed)
        delete_response = self.api.delete(f'/api/resources/{data_returned["id"]}')
        self.assertEqual(delete_response.status_code, 200)


    def test_create_resource_with_bad_request(self):
        """
        Test POST /api/departments/<department_id>/resources/ endpoint with non-json
        content-type
        """
        resource_info = {"title": "Bad Resource",
                         "content": "An example bad resource for testing",
                         "teacher_id": self.teacher.id}
        fake_resource_info = {"title": "Fake Resource",
                              "content": "This is a fake resource",
                              "teacher_id": "567890987654"}
        response = self.api.post(f"/api/teachers/{self.teacher.id}/resources/",
                                 data=resource_info,
                                 content_type="application/json")
        response2 = self.api.post(f"/api/teachers/{self.teacher.id}/resources/",
                                  data=json.dumps(resource_info),
                                  content_type="^/application/json")
        response3 = self.api.post(f"/api/teachers/{self.teacher.id}/resources/",
                                  data=json.dumps(fake_resource_info),
                                  content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_update_resource(self):
        """ Test PUT /api/resource/<resource_id>" endpoint """
        response = self.api.put(f"/api/resources/{self.resource.id}",
                                data=json.dumps({"title": "Updated Resource"}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned["title"], "Updated Resource")

        # Check that update is visible in storage
        resource = storage.get(Resource, self.resource.id)
        self.assertEqual(resource.title, "Updated Resource")


if __name__ == "__main__":
    unittest.main()

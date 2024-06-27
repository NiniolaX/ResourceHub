#!/usr/bin/python3
""" Tests the department view of the API """
from api.api import api
from api.models import storage
from api.models.department import Department
from api.models.school import School
from os import getenv
import json
import unittest


class DepartmentApiTestCase(unittest.TestCase):
    """ Tests the department view of the API """
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
        self.school.save()
        self.department.save()

    def tearDown(self):
        """ Cleans up test environment """
        self.department.delete()
        self.school.delete()
        storage.close()
        self.api_context.pop()

    def test_get_departments(self):
        """ Test GET /api/schools/<school_id>/departments endpoint """
        response = self.api.get(f"/api/schools/{self.school.id}/departments/")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        # Check that department object exists in data returned
        self.assertIn(self.department.to_dict(), data_returned)
        # Check that object of different class does not exist in data returned
        other_classes = ["School", "Teacher", "Learner", "Resource"]
        for obj in data_returned:
            self.assertTrue(obj["__class__"] not in other_classes)

    def test_get_department(self):
        """ Test GET /api/departments/<department_id> endpoint """
        response = self.api.get(f"/api/departments/{self.department.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, self.department.to_dict())

    def test_delete_department(self):
        """ Test DELETE /api/departments/<department_id> endpoint """
        response = self.api.delete(f"/api/departments/{self.department.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_department(self):
        """ Test POST /api/schools/<school_id>/departments/ endpoint """
        # Create new department via API
        new_department_info = {"name": "New Department",
                               "school_id": self.school.id}
        create_response = self.api.post(f"/api/schools/{self.school.id}/departments/",
                                        data=json.dumps(new_department_info),
                                        content_type="application/json")
        # Check response of API query
        self.assertEqual(create_response.status_code, 201)
        data_returned = json.loads(create_response.data)
        self.assertIn("id", data_returned)
        self.assertEqual(data_returned["name"], "New Department")

        # Check that new object is in storage
        department_id = data_returned["id"]
        self.assertIn(f'Department.{department_id}', storage.all(Department))

        # Delete new department via api (no duplicate departments allowed)
        delete_response = self.api.delete(f'/api/departments/{data_returned["id"]}')
        self.assertEqual(delete_response.status_code, 200)

    def test_create_existing_department(self):
        """
        Test POST /api/schools/<school_id>/departments/ endpoint with existing
        department
        """
        existing_department_info = {"name": "Test Department",
                                    "school_id": self.school.id}
        response = self.api.post(f"/api/schools/{self.school.id}/departments/",
                                 data=json.dumps(existing_department_info),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_department_with_bad_request(self):
        """
        Test POST /api/schools/<school_id>/departments/ endpoint with non-json
        content-type
        """
        department_info = {"name": "Bad Department",
                           "school_id": self.school.id}
        fake_department_info = {"name": "Fake Department",
                                "school_id": "567890987654"}
        response = self.api.post(f"/api/schools/{self.school.id}/departments/",
                                 data=department_info,
                                 content_type="application/json")
        response2 = self.api.post(f"/api/schools/{self.school.id}/departments/",
                                  data=json.dumps(department_info),
                                  content_type="^/application/json")
        response3 = self.api.post(f"/api/schools/{fake_department_info['school_id']}/departments/",
                                  data=json.dumps(fake_department_info),
                                  content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response3.status_code, 404)

    def test_update_department(self):
        """ Test PUT /api/department/<department_id>" endpoint """
        response = self.api.put(f"/api/departments/{self.department.id}",
                                data=json.dumps({"name": "Updated Department"}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned["name"], "Updated Department")

        # Check that update is visible in storage
        department = storage.get(Department, self.department.id)
        self.assertEqual(department.name, "Updated Department")


if __name__ == "__main__":
    unittest.main()

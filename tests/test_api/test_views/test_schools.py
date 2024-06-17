#!/usr/bin/python3
""" Tests the school view of the API """
import unittest
import json
from api.api import api
from models import storage
from models.school import School
from os import getenv
from werkzeug.security import check_password_hash


class SchoolApiTestCase(unittest.TestCase):
    """ Tests the school view of the API """
    def setUp(self):
        """ Sets up test environment """
        self.api = api.test_client()
        self.api.testing = True

        # Create application context
        self.api_context = api.app_context()
        self.api_context.push()

        # Initialize storage
        storage.reload()

        # Create test school object
        self.school = School(name="Test School",
                             email="test@gmail.com",
                             password="123")
        self.school.save()

    def tearDown(self):
        """ Cleans up test environment """
        self.school.delete()
        storage.close()
        self.api_context.pop()

    def test_get_schools(self):
        """ Test GET /api/schools endpoint """
        response = self.api.get("/api/schools/")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        # Check that school object exists in data returned
        self.assertIn(self.school.to_dict(), data_returned)
        # Check that object of different class does not exist in data returned
        other_classes = ["Department", "Teacher", "Learner", "Resource"]
        for obj in data_returned:
            self.assertTrue(obj["__class__"] not in other_classes)

    def test_get_school(self):
        """ Test GET /api/schools/<school_id> endpoint """
        response = self.api.get(f"/api/schools/{self.school.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, self.school.to_dict())

    def test_delete_school(self):
        """ Test DELETE /api/schools/<school_id> endpoint """
        response = self.api.delete(f"/api/schools/{self.school.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_school(self):
        """ Test POST /api/schools/ endpoint """
        # Create new school via API
        new_school_info = {"name": "New School",
                           "email": "new_school@gmail.com",
                           "password": "123456"}
        create_response = self.api.post("/api/schools/",
                                        data=json.dumps(new_school_info),
                                        content_type="application/json")
        # Check response of API query
        self.assertEqual(create_response.status_code, 201)
        data_returned = json.loads(create_response.data)
        self.assertIn("id", data_returned)
        self.assertEqual(data_returned["name"], "New School")
        self.assertEqual(data_returned["email"], "new_school@gmail.com")
        self.assertTrue(check_password_hash(data_returned["password"],
                        new_school_info["password"]))

        # Check that new object is in storage
        school_id = data_returned["id"]
        self.assertIn(f'School.{school_id}', storage.all(School))

        # Delete new school via api (no duplicate schools allowed)
        delete_response = self.api.delete(f'/api/schools/{data_returned["id"]}')
        self.assertEqual(delete_response.status_code, 200)

    def test_create_existing_school(self):
        """ Test POST /api/schools/ endpoint with existing school """
        existing_school_info = {"name": "Test School",
                                "email": "test@gmail.com",
                                "password": "123"}
        response = self.api.post("/api/schools/",
                                 data=json.dumps(existing_school_info),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_school_with_bad_request(self):
        """ Test POST /api/schools/ endpoint with non-json content-type """
        school_info = {"name": "Bad School",
                       "email": "bad@gmail.com",
                       "password": "12345678"}
        response = self.api.post("/api/schools/",
                                 data=school_info,
                                 content_type="application/json")
        response2 = self.api.post("/api/schools/",
                                  data=json.dumps(school_info),
                                  content_type="^/application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_update_school(self):
        """ Test PUT /api/school/<school_id>" endpoint """
        response = self.api.put(f"/api/schools/{self.school.id}",
                                data=json.dumps({"name": "Updated School"}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned["name"], "Updated School")

        # Check that update is visible in storage
        school = storage.get(School, self.school.id)
        self.assertEqual(school.name, "Updated School")


if __name__ == "__main__":
    unittest.main()

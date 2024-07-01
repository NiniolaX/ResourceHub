#!/usr/bin/python3
""" Tests the learner view of the API """
import unittest
import json
from api.api import api
from api.models import storage
from api.models.learner import Learner
from api.models.department import Department
from api.models.school import School
from os import getenv


class LearnerApiTestCase(unittest.TestCase):
    """ Tests the learners view of the API """
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
        self.learner = Learner(fname="Test",
                               lname="Learner",
                               email="test01@gmail.com",
                               password="123",
                               department_id=self.department.id,
                               school_id=self.school.id)
        self.school.save()
        self.department.save()
        self.learner.save()

    def tearDown(self):
        """ Cleans up test environment """
        self.learner.delete()
        self.department.delete()
        self.school.delete()
        storage.close()
        self.api_context.pop()

    def test_resources_created(self):
        """Check that test objects exist in storage"""
        self.assertIn(self.school, storage.all(School).values())
        self.assertIn(self.department, storage.all(Department).values())
        self.assertIn(self.learner, storage.all(Learner).values())

    def test_get_learners(self):
        """ Test GET /api/departments/<department_id>/learners endpoint """
        response = self.api.get(f"/api/departments/{self.department.id}/learners/")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        # Check that learner object exists in data returned
        self.assertIn(self.learner.to_dict(), data_returned)
        # Check that object of different class does not exist in data returned
        other_classes = ["School", "Department", "Teacher", "Resource"]
        for obj in data_returned:
            self.assertTrue(obj["__class__"] not in other_classes)

    def test_get_learner(self):
        """ Test GET /api/learners/<learner_id> endpoint """
        response = self.api.get(f"/api/learners/{self.learner.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, self.learner.to_dict())

    def test_delete_learner(self):
        """ Test DELETE /api/learners/<learner_id> endpoint """
        response = self.api.delete(f"/api/learners/{self.learner.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_learner(self):
        """ Test POST /api/departments/<department_id>/learners/ endpoint """
        # Create new learner via API
        new_learner_info = {"fname": "New",
                            "lname": "Learner",
                            "email": "test02@gmail.com",
                            "password": "12345",
                            "department_id": self.department.id,
                            "school_id": self.school.id}
        create_response = self.api.post(f"/api/departments/{self.department.id}/learners/",
                                        data=json.dumps(new_learner_info),
                                        content_type="application/json")
        # Check response of API query
        self.assertEqual(create_response.status_code, 201)
        data_returned = json.loads(create_response.data)
        self.assertIn("id", data_returned)
        self.assertEqual(data_returned["fname"], "New")
        self.assertEqual(data_returned["lname"], "Learner")
        self.assertEqual(data_returned["email"], "test02@gmail.com")
        self.assertEqual(data_returned["fname"], "New")
        self.assertTrue(data_returned["password"], "12345")

        # Check that new object is in storage
        learner_id = data_returned["id"]
        self.assertIn(f'Learner.{learner_id}', storage.all(Learner))

        # Delete new learner via api (no duplicate learners allowed)
        delete_response = self.api.delete(f'/api/learners/{data_returned["id"]}')
        self.assertEqual(delete_response.status_code, 200)

    def test_create_existing_learner(self):
        """
        Test POST /api/departments/<department_id>/learners/ endpoint with existing
        learner
        """
        existing_learner_info = {"fname": "Test",
                                 "lname": "Learner",
                                 "email": "test01@gmail.com",
                                 "password": "123",
                                 "department_id": self.department.id,
                                 "school_id": self.school.id}
        response = self.api.post(f"/api/departments/{self.department.id}/learners/",
                                 data=json.dumps(existing_learner_info),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_learner_with_bad_request(self):
        """
        Test POST /api/departments/<department_id>/learners/ endpoint with non-json
        content-type
        """
        learner_info = {"fname": "Bad",
                        "lname":"Learner",
                        "email": "test03@gmail.com",
                        "password": "1234",
                        "department_id": self.department.id,
                        "school_id": self.school.id}
        fake_learner_info = {"fname": "Fake",
                             "lname": "Learner",
                             "email": "test05@gmail.com",
                             "password": "1234",
                             "department_id": "567890987654",
                             "school_id": self.school.id}
        response = self.api.post(f"/api/departments/{self.department.id}/learners/",
                                 data=learner_info,
                                 content_type="application/json")
        response2 = self.api.post(f"/api/departments/{self.department.id}/learners/",
                                  data=json.dumps(learner_info),
                                  content_type="^/application/json")
        response3 = self.api.post(f"/api/departments/{self.department.id}/learners/",
                                  data=json.dumps(fake_learner_info),
                                  content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_update_learner(self):
        """ Test PUT /api/learner/<learner_id>" endpoint """
        response = self.api.put(f"/api/learners/{self.learner.id}",
                                data=json.dumps({"fname": "Updated"}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned["fname"], "Updated")

        # Check that update is visible in storage
        learner = storage.get(Learner, self.learner.id)
        self.assertEqual(learner.fname, "Updated")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python3
""" Tests the teacher view of the API """
import unittest
import json
from api.api import api
from models import storage
from models.teacher import Teacher
from models.department import Department
from models.school import School
from os import getenv
from werkzeug.security import check_password_hash


class TeacherApiTestCase(unittest.TestCase):
    """ Tests the teachers view of the API """
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
        self.school.save()
        self.department.save()
        self.teacher.save()

    def tearDown(self):
        """ Cleans up test environment """
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

    def test_get_teachers(self):
        """ Test GET /api/departments/<department_id>/teachers endpoint """
        response = self.api.get(f"/api/departments/{self.department.id}/teachers/")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        # Check that teacher object exists in data returned
        self.assertIn(self.teacher.to_dict(), data_returned)
        # Check that object of different class does not exist in data returned
        other_classes = ["School", "Department", "Learner", "Resource"]
        for obj in data_returned:
            self.assertTrue(obj["__class__"] not in other_classes)

    def test_get_teacher(self):
        """ Test GET /api/teachers/<email> endpoint """
        response = self.api.get(f"/api/teachers/{self.teacher.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, self.teacher.to_dict())

    def test_delete_teacher(self):
        """ Test DELETE /api/teachers/<teacher_id> endpoint """
        response = self.api.delete(f"/api/teachers/{self.teacher.id}")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned, {})

    def test_create_teacher(self):
        """ Test POST /api/departments/<department_id>/teachers/ endpoint """
        # Create new teacher via API
        new_teacher_info = {"fname": "New",
                            "lname": "Teacher",
                            "email": "test02@gmail.com",
                            "password": "12345",
                            "department_id": self.department.id,
                            "school_id": self.school.id}
        create_response = self.api.post(f"/api/departments/{self.department.id}/teachers/",
                                        data=json.dumps(new_teacher_info),
                                        content_type="application/json")
        # Check response of API query
        self.assertEqual(create_response.status_code, 201)
        data_returned = json.loads(create_response.data)
        self.assertIn("id", data_returned)
        self.assertEqual(data_returned["fname"], "New")
        self.assertEqual(data_returned["lname"], "Teacher")
        self.assertEqual(data_returned["email"], "test02@gmail.com")
        self.assertEqual(data_returned["fname"], "New")
        self.assertEqual(data_returned["password"], "12345")

        # Check that new object is in storage
        teacher_id = data_returned["id"]
        self.assertIn(f'Teacher.{teacher_id}', storage.all(Teacher))

        # Delete new teacher via api (no duplicate teachers allowed)
        delete_response = self.api.delete(f'/api/teachers/{data_returned["id"]}')
        self.assertEqual(delete_response.status_code, 200)

    def test_create_existing_teacher(self):
        """
        Test POST /api/departments/<department_id>/teachers/ endpoint with existing
        teacher
        """
        existing_teacher_info = {"fname": "Test",
                                 "lname": "Teacher",
                                 "email": "test01@gmail.com",
                                 "password": "123",
                                 "department_id": self.department.id,
                                 "school_id": self.school.id}
        response = self.api.post(f"/api/departments/{self.department.id}/teachers/",
                                 data=json.dumps(existing_teacher_info),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_teacher_with_bad_request(self):
        """
        Test POST /api/departments/<department_id>/teachers/ endpoint with non-json
        content-type
        """
        teacher_info = {"fname": "Bad",
                        "lname":"Teacher",
                        "email": "test03@gmail.com",
                        "password": "1234",
                        "department_id": self.department.id,
                        "school_id": self.school.id}
        fake_teacher_info = {"fname": "Fake",
                             "lname": "Teacher",
                             "email": "test05@gmail.com",
                             "password": "1234",
                             "department_id": "567890987654",
                             "school_id": self.school.id}
        response = self.api.post(f"/api/departments/{self.department.id}/teachers/",
                                 data=teacher_info,
                                 content_type="application/json")
        response2 = self.api.post(f"/api/departments/{self.department.id}/teachers/",
                                  data=json.dumps(teacher_info),
                                  content_type="^/application/json")
        response3 = self.api.post(f"/api/departments/{self.department.id}/teachers/",
                                  data=json.dumps(fake_teacher_info),
                                  content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response2.status_code, 400)

    def test_update_teacher(self):
        """ Test PUT /api/teacher/<teacher_id>" endpoint """
        response = self.api.put(f"/api/teachers/{self.teacher.id}",
                                data=json.dumps({"fname": "Updated"}),
                                content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data_returned = json.loads(response.data)
        self.assertEqual(data_returned["fname"], "Updated")

        # Check that update is visible in storage
        teacher = storage.get(Teacher, self.teacher.id)
        self.assertEqual(teacher.fname, "Updated")


if __name__ == "__main__":
    unittest.main()

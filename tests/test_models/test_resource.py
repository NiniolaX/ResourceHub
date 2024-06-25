#!/usr/bin/python3
"""
Contains unittests for the Resource class
"""

from datetime import datetime
import inspect
import models
from models.base_model import BaseModel
from models.department import Department
from models.resource import Resource
from models.school import School
from models.teacher import Teacher
import unittest


class TestResourceDocs(unittest.TestCase):
    """Test to check the documentation and style of Resource class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.resource_f = inspect.getmembers(Resource, inspect.isfunction)

    def test_resource_class_docstring(self):
        """Test for the Resource clasdocstring"""
        self.assertIsNot(Resource.__doc__, None,
                         "Resource clasneeds a docstring")
        self.assertTrue(len(Resource.__doc__) >= 1,
                        "Resource clasneeds a docstring")

    def test_resource_func_docstrings(self):
        """Test for the presence of docstring in Resource methods"""
        for func in self.resource_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needa docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needa docstring".format(func[0]))


class TestResource(unittest.TestCase):
    """Test the Resource class"""
    def setUp(self):
        """Sets up test resources"""
        self.school = School(name="Havard University",
                             email="havard@gmail.com",
                             password="harvard123")
        self.dept = Department(name="Department of Computer Science",
                               school_id=self.school.id)
        self.teacher = Teacher(fname="Love", lname="Afinni",
                               email="loveafinni@gmail.com",
                               password="12345678",
                               department_id=self.dept.id,
                               school_id=self.school.id)
        self.resource = Resource(title="Data Structures and Algorithms",
                                 content="""
                                 A data structure is a way to store data.
                                 We structure data in different ways depending
                                 on what data we have, and what we want to do
                                 with it.""",
                                 slug="abcdefghij",
                                 teacher_id=self.teacher.id,
                                 department_id=self.dept.id,
                                 school_id=self.school.id)
        self.school.save()
        self.dept.save()
        self.teacher.save()
        self.resource.save()

    def tearDown(self):
        """Cleans up test resources"""
        self.resource.delete()
        self.teacher.delete()
        self.dept.delete()
        self.school.delete()
        models.storage.close()

    def test_is_subclass(self):
        """Test that Resource is subclass of BaseModel"""
        self.assertIsInstance(self.resource, BaseModel)
        self.assertTrue(hasattr(self.resource, "id"))
        self.assertTrue(hasattr(self.resource, "created_at"))
        self.assertTrue(hasattr(self.resource, "updated_at"))

    def test_attrs(self):
        """Test the Resource attributes"""
        self.assertTrue(hasattr(self.resource, "title"))
        self.assertTrue(hasattr(self.resource, "content"))
        self.assertTrue(hasattr(self.resource, "slug"))
        self.assertTrue(hasattr(self.resource, "teacher_id"))
        self.assertTrue(hasattr(self.resource, "department_id"))
        self.assertTrue(hasattr(self.resource, "school_id"))
        self.assertTrue(hasattr(self.resource, "teacher"))
        self.assertEqual(self.resource.title, "Data Structures and Algorithms")

    def test_to_dict_creates_dict(self):
        """test to_dict method createa dictionary with proper attrs"""
        new_d = self.resource.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in self.resource.__dict__:
            if attr != "_sa_instance_state":
                self.assertIn(attr, new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that valuein dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.resource.to_dict()
        self.assertEqual(new_d["__class__"], "Resource")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         self.resource.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         self.resource.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method hathe correct output"""
        string = "[Resource] ({}) {}".format(self.resource.id,
                                             self.resource.__dict__)
        self.assertEqual(string, str(self.resource))

#!/usr/bin/python3
"""
Contains unittests for the Teacher class
"""

from api import models
from api.models.base_model import BaseModel
from api.models.department import Department
from api.models.school import School
from api.models.teacher import Teacher
from datetime import datetime
import inspect
import unittest


class TestTeacherDocs(unittest.TestCase):
    """Test to check the documentation and style of Teacher class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.teacher_f = inspect.getmembers(Teacher, inspect.isfunction)

    def test_teacher_class_docstring(self):
        """Test for the Teacher clasdocstring"""
        self.assertIsNot(Teacher.__doc__, None,
                         "Teacher clasneeds a docstring")
        self.assertTrue(len(Teacher.__doc__) >= 1,
                        "Teacher clasneeds a docstring")

    def test_teacher_func_docstrings(self):
        """Test for the presence of docstring in Teacher methods"""
        for func in self.teacher_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needa docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needa docstring".format(func[0]))


class TestTeacher(unittest.TestCase):
    """Test the Teacher class"""
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
        self.school.save()
        self.dept.save()
        self.teacher.save()

    def tearDown(self):
        """Cleans up test resources"""
        self.teacher.delete()
        self.dept.delete()
        self.school.delete()
        models.storage.close()

    def test_is_subclass(self):
        """Test that Teacher is subclass of BaseModel"""
        self.assertIsInstance(self.teacher, BaseModel)
        self.assertTrue(hasattr(self.teacher, "id"))
        self.assertTrue(hasattr(self.teacher, "created_at"))
        self.assertTrue(hasattr(self.teacher, "updated_at"))

    def test_attrs(self):
        """Test the Teacher attributes"""
        self.assertTrue(hasattr(self.teacher, "fname"))
        self.assertTrue(hasattr(self.teacher, "lname"))
        self.assertTrue(hasattr(self.teacher, "email"))
        self.assertTrue(hasattr(self.teacher, "password"))
        self.assertTrue(hasattr(self.teacher, "department_id"))
        self.assertTrue(hasattr(self.teacher, "school_id"))
        self.assertTrue(hasattr(self.teacher, "resources"))
        self.assertEqual(self.teacher.fname, "Love")
        self.assertEqual(self.teacher.lname, "Afinni")
        self.assertEqual(self.teacher.email, "loveafinni@gmail.com")

    def test_to_dict_creates_dict(self):
        """test to_dict method createa dictionary with proper attrs"""
        new_d = self.teacher.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in self.teacher.__dict__:
            if attr != "_sa_instance_state":
                self.assertIn(attr, new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that valuein dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.teacher.to_dict()
        self.assertEqual(new_d["__class__"], "Teacher")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         self.teacher.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         self.teacher.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method hathe correct output"""
        string = "[Teacher] ({}) {}".format(self.teacher.id,
                                            self.teacher.__dict__)
        self.assertEqual(string, str(self.teacher))

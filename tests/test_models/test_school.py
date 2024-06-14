#!/usr/bin/python3
"""
Contains unittests for the School class
"""

from datetime import datetime
import inspect
import models
from models.base_model import BaseModel
from models.school import School
import unittest


class TestSchoolDocs(unittest.TestCase):
    """Tests to check the documentation and style of School class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.school_f = inspect.getmembers(School, inspect.isfunction)

    def test_school_class_docstring(self):
        """Test for the School class docstring"""
        self.assertIsNot(School.__doc__, None,
                         "School class needs a docstring")
        self.assertTrue(len(School.__doc__) >= 1,
                        "School class needs a docstring")

    def test_school_func_docstrings(self):
        """Test for the presence of docstrings in School methods"""
        for func in self.school_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestSchool(unittest.TestCase):
    """Test the School class"""
    def setUp(self):
        self.school = School(name="University of Jos",
                        email="unijos@gmail.com",
                        password="12345678")

    def tearDown(self):
        self.school.delete()

    def test_is_subclass(self):
        """Test that School is a subclass of BaseModel"""
        self.assertIsInstance(self.school, BaseModel)
        self.assertTrue(hasattr(self.school, "id"))
        self.assertTrue(hasattr(self.school, "created_at"))
        self.assertTrue(hasattr(self.school, "updated_at"))

    def test_name_attr(self):
        """Test that School has attribute name, and it's as an empty string"""
        self.assertTrue(hasattr(self.school, "name"))
        self.assertEqual(self.school.name, "University of Jos")

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        new_d = self.school.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_school" in new_d)
        for attr in s.__dict__:
            if attr is not "_sa_instance_school":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.school.to_dict()
        self.assertEqual(new_d["__class__"], "School")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        string = "[School] ({}) {}".format(self.school.id, self.school.__dict__)
        self.assertEqual(string, str(self.school))

#!/usr/bin/python3
"""
Contains unittests for the Department class
"""

from datetime import datetime
import inspect
import models
from models.base_model import BaseModel
from models.department import Department
from models.school import School
import unittest


class TestDepartmentDocs(unittest.TestCase):
    """Test to check the documentation and style of Department class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dept_f = inspect.getmembers(Department, inspect.isfunction)

    def test_dept_class_docstring(self):
        """Test for the Department clasdocstring"""
        self.assertIsNot(Department.__doc__, None,
                         "Department clasneeds a docstring")
        self.assertTrue(len(Department.__doc__) >= 1,
                        "Department clasneeds a docstring")

    def test_dept_func_docstrings(self):
        """Test for the presence of docstringin Department methods"""
        for func in self.dept_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needa docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needa docstring".format(func[0]))


class TestDepartment(unittest.TestCase):
    """Test the Department class"""
    def setUp(self):
        self.school = School(name="Tai Solarin University of Education",
                             email="tasued@gmail.com",
                             password="tasued456")
        self.dept = Department(name="Department of Physics",
                               school_id=self.school.id)
        self.school.save()
        self.dept.save()

    def tearDown(self):
        self.dept.delete()
        self.school.delete()
        models.storage.close()

    def test_is_subclass(self):
        """Test that Department is subclass of BaseModel"""
        self.assertIsInstance(self.dept, BaseModel)
        self.assertTrue(hasattr(self.dept, "id"))
        self.assertTrue(hasattr(self.dept, "created_at"))
        self.assertTrue(hasattr(self.dept, "updated_at"))

    def test_attrs(self):
        """Test the Department attributes"""
        self.assertTrue(hasattr(self.dept, "name"))
        self.assertTrue(hasattr(self.dept, "school_id"))
        self.assertTrue(hasattr(self.dept, "teachers"))
        self.assertTrue(hasattr(self.dept, "learners"))
        self.assertTrue(hasattr(self.dept, "resources"))
        self.assertEqual(self.dept.name, "Department of Physics")
        self.assertEqual(self.dept.school_id, self.school.id)

    def test_to_dict_creates_dict(self):
        """test to_dict method createa dictionary with proper attrs"""
        new_d = self.dept.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in self.dept.__dict__:
            if attr != "_sa_instance_state":
                self.assertIn(attr, new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that valuein dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.dept.to_dict()
        self.assertEqual(new_d["__class__"], "Department")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         self.dept.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         self.dept.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method hathe correct output"""
        string = "[Department] ({}) {}".format(self.dept.id,
                                               self.dept.__dict__)
        self.assertEqual(string, str(self.dept))

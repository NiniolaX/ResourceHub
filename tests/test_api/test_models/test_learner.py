#!/usr/bin/python3
"""
Contains unittests for the Learner class
"""

from api import models
from api.models.base_model import BaseModel
from api.models.department import Department
from api.models.learner import Learner
from api.models.school import School
from datetime import datetime
import inspect
import unittest


class TestLearnerDocs(unittest.TestCase):
    """Test to check the documentation and style of Learner class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.learner_f = inspect.getmembers(Learner, inspect.isfunction)

    def test_learner_class_docstring(self):
        """Test for the Learner clasdocstring"""
        self.assertIsNot(Learner.__doc__, None,
                         "Learner clasneeds a docstring")
        self.assertTrue(len(Learner.__doc__) >= 1,
                        "Learner clasneeds a docstring")

    def test_learner_func_docstrings(self):
        """Test for the presence of docstring in Learner methods"""
        for func in self.learner_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needa docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needa docstring".format(func[0]))


class TestLearner(unittest.TestCase):
    """Test the Learner class"""
    def setUp(self):
        """Sets up test resources"""
        self.school = School(name="Havard University",
                             email="havard@gmail.com",
                             password="harvard123")
        self.dept = Department(name="Department of Computer Science",
                               school_id=self.school.id)
        self.learner = Learner(fname="Quyum", lname="Ajumobi",
                               email="quyumajumobi@gmail.com",
                               password="12345678",
                               department_id=self.dept.id,
                               school_id=self.school.id)
        self.school.save()
        self.dept.save()
        self.learner.save()

    def tearDown(self):
        """Cleans up test resources"""
        self.learner.delete()
        self.dept.delete()
        self.school.delete()
        models.storage.close()

    def test_is_subclass(self):
        """Test that Learner is subclass of BaseModel"""
        self.assertIsInstance(self.learner, BaseModel)
        self.assertTrue(hasattr(self.learner, "id"))
        self.assertTrue(hasattr(self.learner, "created_at"))
        self.assertTrue(hasattr(self.learner, "updated_at"))

    def test_attrs(self):
        """Test the Learner attributes"""
        self.assertTrue(hasattr(self.learner, "fname"))
        self.assertTrue(hasattr(self.learner, "lname"))
        self.assertTrue(hasattr(self.learner, "email"))
        self.assertTrue(hasattr(self.learner, "password"))
        self.assertTrue(hasattr(self.learner, "department_id"))
        self.assertTrue(hasattr(self.learner, "school_id"))
        self.assertEqual(self.learner.fname, "Quyum")
        self.assertEqual(self.learner.lname, "Ajumobi")
        self.assertEqual(self.learner.email, "quyumajumobi@gmail.com")

    def test_to_dict_creates_dict(self):
        """test to_dict method createa dictionary with proper attrs"""
        new_d = self.learner.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in self.learner.__dict__:
            if attr != "_sa_instance_state":
                self.assertIn(attr, new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that valuein dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.learner.to_dict()
        self.assertEqual(new_d["__class__"], "Learner")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         self.learner.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         self.learner.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        string = "[Learner] ({}) {}".format(self.learner.id,
                                            self.learner.__dict__)
        self.assertEqual(string, str(self.learner))

#!/usr/bin/python3
""" Unittest for DBStorage class """
import unittest
import MySQLdb
import os
#from console import HBNBCommand
#from models.state import State
from models.school import School
from models import storage


class test_dbStorage(unittest.TestCase):
    """ Class to test database storage """
    def setUp(self):
        """ Set up test resources """
        self.db = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                  port=3306,
                                  user=os.getenv('HBNB_MYSQL_USER'),
                                  passwd=os.getenv('HBNB_MYSQL_PWD'),
                                  database=os.getenv('HBNB_MYSQL_DB')
                                  )
        self.cur = self.db.cursor()
        storage.reload()
        #self.console = HBNBCommand()

    def tearDown(self):
        """ Cleans up test resources """
        self.cur.close()
        self.db.close()

    def test_new(self):
        """ Tests the new method """
        #self.console.do_create('State name="Osun"')
        school = School(name="University of Lagos", email="unilag@gmail.com",
                        password="123")
        school.save()
        self.assertIn(school, storage.all(School).values())
        school.delete()
        storage.save()

    def test_save(self):
        """ Tests the save method """
        #self.cur.execute('SELECT COUNT(*) FROM states')
        initial_count = storage.count(School)
        #self.console.do_create('State name="Abuja"')
        school = School(name="University of Lagos", email="unilag@gmail.com",
                        password="123")
        storage.save(school)
        # Confirm that object was saved
        self.assertIn(school, storage.all(School).values())
        storage.close()  # SQL alchemy didn't reload his 'Session' so close
        #self.cur.execute('SELECT COUNT(*) FROM states')
        final_count = storage.count(School)
        self.assertNotEqual(initial_count, final_count)
        school.delete()
        storage.save()

    def test_get(self):
        """Test that get returns the appropriate object"""
        # Get a storage object
        school = School(name="University of Lagos", email="unilag@gmail.com",
                        password="123")
        school.save()
        school_returned = storage.get(School, school.id)
        self.assertIs(school, school_returned)

    def test_count_with_class(self):
        """Test the count method with class argument"""
        school_count = len(storage.all(School))
        if school_count:
            self.isInstance(school_count, int)
        self.assertEqual(school_count, storage.count(School))

    def test_count_without_class(self):
        """Test the count method without class argument"""
        obj_count = len(storage.all())
        if obj_count:
            self.isInstance(obj_count, int)
        self.assertEqual(obj_count, storage.count())


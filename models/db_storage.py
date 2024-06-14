#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.department import Department
from models.learner import Learner
from models.school import School
from models.teacher import Teacher
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
        "school": School,
        "department": Department,
        "teacher": Teacher,
        "learner": Learner
        }

class DBStorage:
    """Class interacts with MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a DBStorage object"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db))
        if env == "test":
            # Drop all tables
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries current database session
        Args:
            cls(str): Name of class whose table is to be queried (optional)
        Return:
            __objects(dict): Format: {<class-name.obj1-id> = obj,...}
        """
        objects = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    objects[key] = obj
        return (objects)

    def new(self, obj):
        """Adds an object to the current database session
        Args:
            obj(object): Object to be added
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not None
        Args:
            obj(object): Object to be deleted
        Return:
            None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, obj_id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        Args:
            cls(class): Class of object to be retrieved
            obj_id(str): Id of object to be retrieved
        Return:
            obj(object): Object
        """
        # Return None if no class or object was passed
        if not cls or not obj_id:
            return None

        # Return None if class does not exist
        if cls not in classes.values():
            return None

        # Retrieve object
        cls_objs = models.storage.all(cls)
        for obj in cls_objs.values():
            if (obj.id == id):
                return obj
        # Return None if object was not found
        return None

    def count(self, cls=None):
        """Returns the number of objects in storage
        Args:
            cls(class): Class of objects to count
        """
        if not cls:
            return len(models.storage.all().values())
        else:
            return len(models.storage.all(cls).values())

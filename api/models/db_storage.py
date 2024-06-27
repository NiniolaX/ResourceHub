#!/usr/bin/python3
"""
Contains the class DBStorage
"""

#import models
from api.models.base_model import BaseModel, Base
from api.models.department import Department
from api.models.learner import Learner
from api.models.resource import Resource
from api.models.school import School
from api.models.teacher import Teacher
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, registry
import sqlalchemy

classes = {
        "school": School,
        "department": Department,
        "teacher": Teacher,
        "learner": Learner,
        "resource": Resource
        }


class DBStorage:
    """Class interacts with MySQL database"""
    __engine = None
    __session = None

    def __init__(self, DATABASE_URI):
        """Instantiates a DBStorage object"""
        self.__engine = create_engine(DATABASE_URI)  # DATABASE_URI defined and passed in models/__init__.py
        env = environ.get('HUB_ENV')
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
        self.save()

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
            self.save()

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
#        for cls in classes.values():
#            registry.map_imperatively(cls, cls.__table__,
#                                      confirm_deleted_rows=False)

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
        cls_objs = self.all(cls).values()
        for obj in cls_objs:
            if (obj.id == obj_id):
                return obj
        # Return None if object was not found
        return None

    def count(self, cls=None):
        """Returns the number of objects in storage
        Args:
            cls(class): Class of objects to count
        """
        if not cls:
            return len(self.all().values())
        else:
            return len(self.all(cls).values())

    def is_email_unique(self, email):
        """Checks that an email does not already exist in storage
        Args:
            email(str): Email to validate
        Return:
            (bool): True if email does not exist, False if otherwise
        """
        user_models = [School, Teacher, Learner]
        for model in user_models:
            if self.__session.query(model).filter_by(email=email).first():
                return False
        return True

    def get_user_by_email(self, email, user_type=None):
        """Returns a user object by email
        Args:
            email(str): Email of user to fetch
            user_type(str): Type of user
        """
        if not user_type:
            all_users = {**self.all(School), **self.all(Teacher), **self.all(Learner)}
            for user in all_users.values():
                if user.email == email:
                    return user
        else:
            if user_type not in classes:
                return None
            for user in self.all(classes[user_type]).values():
                if user.email == email:
                    return user

        return None

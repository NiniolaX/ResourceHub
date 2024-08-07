#!/usr/bin/python3
"""
Recreates a user object as a subclass of UserMixin from its dictionary
representation.
"""
from flask_login import UserMixin


class GenericUser(UserMixin):
    """ Recreates a user as a subclass of UserMixin
    Params:
        kwargs (dict): dictionary representation of user data
    """
    def __init__(self, **kwargs):
        """ Initializes instance """
        self.__dict__.update(kwargs)

    @property
    def role(self):
        """ Returns user role """
        return self.__dict__.get('__class__') # __class__ parameter was defined in BaseModel

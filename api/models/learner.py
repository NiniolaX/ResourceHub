#!/usr/bin/python3
""" Contains the Learner class"""
from api import models
from api.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy


class Learner(BaseModel, Base):
    """Representation of learner """
    __tablename__ = 'learners'
    fname = Column(String(128), nullable=False)
    lname = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    department_id = Column(String(60), ForeignKey('departments.id'),
                           nullable=False)
    school_id = Column(String(60), ForeignKey('schools.id'),
                       nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes learner"""
        super().__init__(*args, **kwargs)

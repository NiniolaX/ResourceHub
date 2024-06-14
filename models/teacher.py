#!/usr/bin/python3
""" Contains the Teacher class"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Teacher(BaseModel, Base):
    """Representation of teacher """
        __tablename__ = 'teachers'
        fname = Column(String(128), nullable=False)
        lname = Column(String(128), nullable=False)
        email = Column(String(128), unique=True, nullable=False)
        password = Column(String(128), nullable=False)
        department_id = Column(String(60), ForeignKey('departments.id',
                                nullable=False)
        school_id = Column(String(60), ForeignKey('schools.id',
                                nullable=False)
#        resources = relationship("Resource",
#                                backref="teacher",
#                                cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes teacher"""
        super().__init__(*args, **kwargs)

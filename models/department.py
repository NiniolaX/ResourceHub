#!/usr/bin/python3
""" Contains the Department class """
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Department(BaseModel, Base):
    """Representation of department"""
    __tablename__ = 'departments'
    name = Column(String(128), nullable=False)
    school_id = Column(String(60), ForeignKey('schools.id'), nullable=False)
    teachers = relationship("Teacher",
                            backref="department",
                            cascade="all, delete, delete-orphan")
    learners = relationship("Learner",
                            backref="department",
                            cascade="all, delete, delete-orphan")
    resources = relationship("Resource",
                            backref="department",
                            cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes department"""
        super().__init__(*args, **kwargs)

#!/usr/bin/python3
""" Contains the School class"""
import models
from models.base_model import BaseModel, Base
from flask_login import UserMixin
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class School(UserMixin, BaseModel, Base):
    """Representation of school """
    __tablename__ = 'schools'
    name = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    departments = relationship("Department",
                               backref="school",
                               cascade="all, delete, delete-orphan")
    teachers = relationship("Teacher",
                            backref="school",
                            cascade="all, delete, delete-orphan")
    learners = relationship("Learner",
                            backref="school",
                            cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes school"""
        super().__init__(*args, **kwargs)

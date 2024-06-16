#!/usr/bin/python3
""" Contains the Resource class """
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship


class Resource(BaseModel, Base):
    """Representation of resource"""
    __tablename__ = 'resources'
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(Text, nullable=False)
    teacher_id = Column(String(60), ForeignKey('teachers.id'),
                        nullable=False)
    department_id = Column(String(60), ForeignKey('departments.id'),
                           nullable=False)
    school_id = Column(String(60), ForeignKey('schools.id'),
                       nullable=False)
    teacher = relationship("Teacher", back_populates="resources")

    def __init__(self, *args, **kwargs):
        """Initializes resource"""
        super().__init__(*args, **kwargs)

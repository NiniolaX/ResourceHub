#!/usr/bin/python3
"""Initializes the database"""
from api.models.db_storage import DBStorage
from os import environ

# Environment variables for local testing
user = environ.get('HUB_MYSQL_USER')
pwd = environ.get('HUB_MYSQL_PWD')
host = environ.get('HUB_MYSQL_HOST')
db = environ.get('HUB_MYSQL_DB')

DATABASE_URI = environ.get('DATABASE_URL', f'mysql+mysqldb://{user}:{pwd}@{host}/{db}')

# Create instance of storage for application
storage = DBStorage(DATABASE_URI)
storage.reload()

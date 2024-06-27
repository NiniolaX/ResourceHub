#!/usr/bin/python3
"""Initializes the database"""
from models.db_storage import DBStorage
from os import environ

user = environ.get('HUB_MYSQL_USER')
pwd = environ.get('HUB_MYSQL_PWD')
host = environ.get('HUB_MYSQL_HOST')
db = environ.get('HUB_MYSQL_DB')

DATABASE_URI = environ.get('DATABASE_URL', f'mysql+mysqldb://{user}:{pwd}@{host}/{db}')

storage = DBStorage(DATABASE_URI)
storage.reload()

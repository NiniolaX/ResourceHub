#!/usr/bin/python3
"""Initializes the database"""
from models.db_storage import DBStorage
storage = DBStorage()
storage.reload()

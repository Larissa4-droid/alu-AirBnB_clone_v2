#!/usr/bin/python3
"""Test script for DBStorage and State objects"""

from models import storage
from models.state import State

# Retrieve all states from DBStorage
states = storage.all(State)

if states:
    print("OK")


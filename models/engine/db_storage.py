#!/usr/bin/python3
"""Defines the DBStorage engine"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Manages database storage using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Create engine with environment variables"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=True
        )

        # Drop all tables if test environment
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Create all tables in the database and initialize session"""
        # Create tables defined in the Base's subclasses (City, State, etc.)
        Base.metadata.create_all(self.__engine)

        # Create a session
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()


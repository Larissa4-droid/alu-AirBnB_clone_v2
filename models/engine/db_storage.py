#!/usr/bin/python3
"""This is the DBStorage class for AirBnB"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
# Add other models as needed

class DBStorage:
    """Database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Create engine and optionally drop all tables if in test mode"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{password}@{host}/{db}",
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects, or all objects of a specific class"""
        classes = {"State": State, "City": City}
        objects = {}

        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls is None:
                return objects

            for obj in self.__session.query(cls).all():
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj
        else:
            for c in classes.values():
                for obj in self.__session.query(c).all():
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj

        return objects

    def new(self, obj):
        """Add object to session"""
        self.__session.add(obj)

    def save(self):
        """Commit current transaction"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
    from models.base_model import Base
    from models.user import User  # make sure this is imported

    Base.metadata.create_all(self.__engine)    self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                 expire_on_commit=False))()



    def close(self):
        """Close the session"""
        self.__session.close()


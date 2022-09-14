#!/usr/bin/python3
""" Class DBstorage """
import models
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"City": City, "State": State, "User": User, "Place": Place,
           "Review": Review, "Amenity": Amenity}

class DBStorage:
    """ DBStorage """
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HNBN_MYSQL_HOST')
        database = getenv('HNBN_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.format(user,
                                                                                password,
                                                                                host,
                                                                                database), pool_pre_ping=True)

        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        dictionary = {}
        for c in classes:
            if cls is None or cls is classes[c] or cls is c:
                objs = self.__session.query(classes[c]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dictionary[key] = obj
        return (dictionary)

    def new(self.obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(Session)
        self.__session = session()

    def close(self):
        self.__session.close()

    

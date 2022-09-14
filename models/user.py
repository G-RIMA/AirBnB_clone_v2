#!/usr/bin/python3
"""This module defines a class User"""
import hashlib
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if STORAGE_TYPE == 'db':
        __tablename__ = 'users'
        email = Column(string(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))

        places = relationship('Place', backref='user')
        reviews = relationship('Review', backref='user')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """ initiates user """
        if kwargs:
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__set_password(self, pwd)
        super().__init__(*args, **kwargs)

    def __set_password(self, pwd):
        """ custom setter """
        secure = hashlib.md5()
        secure.update(pwd.encode("utf-8"))
        secure_password = secure.hexigest()
        setattr(self, "password", secure_password)

#!/usr/bin/python3
"""
User Class from Models Module
"""

import hashlib
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """
    User class handles all application users
    """

    if STORAGE_TYPE == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', backref='user', cascade='delete')
        reviews = relationship('Review', backref='user', cascade='delete')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """
        Instantiates a User object.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Exceptions:
            None.
        """
        try:
            if kwargs:
                pwd = kwargs.pop('password', None)
                if pwd:
                    User.__set_password(self, pwd)
            super().__init__(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred during User initialization: {str(e)}")

    def __set_password(self, pwd):
        """
        Custom setter: Encrypts the password to MD5.

        Parameters:
            pwd (str): The password to be encrypted.

        Exceptions:
            None.
        """
        try:
            secure = hashlib.md5()
            secure.update(pwd.encode("utf-8"))
            secure_password = secure.hexdigest()
            setattr(self, "password", secure_password)
        except Exception as e:
            print(f"An error occurred during password encryption: {str(e)}")

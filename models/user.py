#!/usr/bin/python3
import hashlib
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    Representation of a user with secure password storage.
    """

    if models.storage == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes a user instance.
        """
        try:
            super().__init__(*args, **kwargs)

            if models.storage_t == 'db':
                self.password = kwargs.get('password', "")

        except Exception as e:
            raise Exception("Error initializing user: " + str(e))

    @property
    def password(self):
        """
        Getter method for password.
        """
        return self.__password

    @password.setter
    def password(self, password):
        """
        Setter method for password. Hashes the password to an MD5 value.
        """
        try:
            if password:
                encoded_password = password.encode('utf-8')
                hashed_password = hashlib.md5(encoded_password).hexdigest()
                self.__password = hashed_password

        except Exception as e:
            raise Exception("Error setting password: " + str(e))

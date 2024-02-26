#!/usr/bin/python3
"""
Database engine
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """
    Handles long-term storage of all class instances.
    """

    CNC = {
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    """
    Handles storage for the database.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database engine.
        """
        try:
            self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                    os.environ.get('HBNB_MYSQL_USER'),
                    os.environ.get('HBNB_MYSQL_PWD'),
                    os.environ.get('HBNB_MYSQL_HOST'),
                    os.environ.get('HBNB_MYSQL_DB')))
            if os.environ.get("HBNB_ENV") == 'test':
                Base.metadata.drop_all(self.__engine)
        except Exception as e:
            raise Exception("Failed to initialize the database engine.") from e

    def all(self, cls=None):
        """
        Returns a dictionary of all objects.

        Parameters:
        - cls (str): The class name (optional).

        Returns:
        - dict: A dictionary of objects with the format "ClassName.object_id".

        Raises:
        - Exception: If an error occurs while fetching the objects.
        """
        try:
            obj_dict = {}
            if cls is not None:
                a_query = self.__session.query(DBStorage.CNC[cls])
                for obj in a_query:
                    obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[obj_ref] = obj
                return obj_dict

            for c in DBStorage.CNC.values():
                a_query = self.__session.query(c)
                for obj in a_query:
                    obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[obj_ref] = obj
            return obj_dict
        except Exception as e:
            raise Exception("Failed to fetch objects from the DB") from e

    def new(self, obj):
        """
        Adds objects to the current database session.

        Parameters:
        - obj (object): The object to be added.

        Raises:
        - Exception: If an error occurs while adding the object.
        """
        try:
            self.__session.add(obj)
        except Exception as e:
            raise Exception("Failed to add object to the database.") from e

    def save(self):
        """
        Commits all changes of the current database session.

        Raises:
        - Exception: If an error occurs while saving changes.
        """
        try:
            self.__session.commit()
        except Exception as e:
            raise Exception("Failed to save changes to the database.") from e

    def rollback_session(self):
        """
        Rolls back a session in the event of an exception.

        Raises:
        - Exception: If an error occurs while rolling back the session.
        """
        try:
            self.__session.rollback()
        except Exception as e:
            raise Exception("Failed to rollback the database session.") from e

    def delete(self, obj=None):
        """
        Deletes an object from the current database session if not None.

        Parameters:
        - obj (object): The object to be deleted (optional).

        Raises:
        - Exception: If an error occurs while deleting the object.
        """
        try:
            if obj:
                self.__session.delete(obj)
                self.save()
        except Exception as e:
            raise Exception("Failed to delete object from
                            the database.") from e

    def delete_all(self):
        """
        Deletes all stored objects (for testing purposes).

        Raises:
        - Exception: If an error occurs while deleting the objects.
        """
        try:
            for c in DBStorage.CNC.values():
                a_query = self.__session.query(c)
                all_objs = [obj for obj in a_query]
                for obj in range(len(all_objs)):
                    to_delete = all_objs.pop(0)
                    to_delete.delete()
            self.save()
        except Exception as e:
            raise Exception("Failed to delete all objects
                            from the database.") from e

    def reload(self):
        """
        Creates all tables in the database and session from the engine.

        Raises:
        - Exception: If an error occurs while reloading the tables and session.
        """
        try:
            Base.metadata.create_all(self.__engine)
            self.__session = scoped_session(
                sessionmaker(
                    bind=self.__engine,
                    expire_on_commit=False))
        except Exception as e:
            raise Exception("Failed to reload the database
                            tables and session.") from e

    def close(self):
        """
        Closes the database session.

        Raises:
        - Exception: If an error occurs while closing the session.
        """
        try:
            self.__session.remove()
        except Exception as e:
            raise Exception("Failed to close the database session.") from e

    def get(self, cls, id):
        """
        Retrieves one object based on class name and id.

        Parameters:
        - cls (str): The class name.
        - id (str): The object id.

        Returns:
        - object: The retrieved object.

        Raises:
        - Exception: If an error occurs while retrieving the object.
        """
        try:
            if cls and id:
                fetch = "{}.{}".format(cls, id)
                all_obj = self.all(cls)
                return all_obj.get(fetch)
            return None
        except Exception as e:
            raise Exception("Failed to retrieve the object
                            from the database.") from e

    def count(self, cls=None):
        """
        Returns the count of all objects in storage.

        Parameters:
        - cls (str): The class name (optional).

        Returns:
        - int: The count of objects.

        Raises:
        - Exception: If an error occurs while counting the objects.
        """
        try:
            return len(self.all(cls))
        except Exception as e:
            raise Exception("Failed to count the objects
                            in the database.") from e

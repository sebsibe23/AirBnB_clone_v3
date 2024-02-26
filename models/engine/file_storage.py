#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""

import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """
    Handles long-term storage of all class instances in JSON format.
    """

    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    """
    CNC - this variable is a dictionary with:
    keys: Class Names
    values: Class type (used for instantiation)
    """

    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects or objects of a specific class.

        Parameters:
        - cls (str): The class name (optional).

        Returns:
        - dict: A dictionary of objects with the format "ClassName.object_id".

        Raises:
        - None.
        """
        if cls is not None:
            new_objs = {}
            for clsid, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    new_objs[clsid] = obj
            return new_objs
        else:
            return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the storage.

        Parameters:
        - obj (object): The object to be added.

        Returns:
        - None.

        Raises:
        - None.
        """
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """
        Serializes the objects to a JSON file.

        Parameters:
        - None.

        Returns:
        - None.

        Raises:
        - Exception: If an error occurs while saving the objects.
        """
        try:
            fname = FileStorage.__file_path
            storage_d = {}
            for bm_id, bm_obj in FileStorage.__objects.items():
                storage_d[bm_id] = bm_obj.to_json(saving_file_storage=True)
            with open(fname, mode='w', encoding='utf-8') as f_io:
                json.dump(storage_d, f_io)
        except Exception as e:
            raise Exception("Failed to save the objects
                            to the JSON file.") from e

    def reload(self):
        """
        Deserializes the JSON file to objects.

        Parameters:
        - None.

        Returns:
        - None.

        Raises:
        - None.
        """
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except Exception as e:
            raise Exception("Failed to delete the object
                            from the storage.") from e
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """
        Deletes an object from the storage.

        Parameters:
        - obj (object): The object to be deleted (optional).

        Returns:
        - None.

        Raises:
        - Exception: If an error occurs while deleting the object.
        """
        try:
            if obj:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                all_class_objs = self.all(obj.__class__.__name__)
                if all_class_objs.get(obj_ref):
                    del FileStorage.__objects[obj_ref]
                self.save()
        except Exception as e:
            raise Exception("Failed to delete the object
                            from the storage.") from e

    def delete_all(self):
        """
        Deletes all stored objects from the storage.

        Parameters:
        - None.

        Returns:
        - None.

        Raises:
        - Exception: If an error occurs while deleting the objects.
        """
        try:
            with open(FileStorage.__file_path, mode='w') as f_io:
                pass
        except Exception as e:
            raise Exception("Failed to delete all
                            objects from the storage.") from e
        del FileStorage.__objects
        FileStorage.__objects = {}
        self.save()

    def close(self):
        """
        Closes the storage and reloads the objects.

        Parameters:
        - None.

        Returns:
        - None.

        Raises:
        - Exception: If an error occurs while closing the storage.
        """
        try:
            self.reload()
        except Exception as e:
            raise Exception("Failed to close the storage.")from e

    def get(self, cls, id):
        """
        Retrieves an object based on the class name and id.

        Parameters:
        - cls (str): The class name.
        - id (str): The id of the object.

        Returns:
        - object: The retrieved object or None if not found.

        Raises:
        - None.
        """
        if cls and id:
            fetch_obj = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch_obj)
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in the storage.

        Parameters:
        - cls (str): The class name (optional).

        Returns:
        - int: The number of objects.

        Raises:
        - None.
        """
        return len(self.all(cls))

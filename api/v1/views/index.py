#!/usr/bin/python3
'''
Use Blueprint instance
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def return_status():
    '''
    Returns the status code
    '''
    try:
        return jsonify(status="OK")
    except Exception as e:
        return jsonify(error=str(e)), 500


@app_views.route('/stats', strict_slashes=False)
def obj_count():
    '''
    Returns the count of objects
    '''
    try:
        amenity = storage.count(Amenity)
        city = storage.count(City)
        place = storage.count(Place)
        review = storage.count(Review)
        state = storage.count(State)
        user = storage.count(User)
        object_dict = {'amenities': amenity, 'cities': city, 'places': place,
                       'reviews': review, 'states': state, 'users': user}
        return jsonify(object_dict)
    except Exception as e:
        return jsonify(error=str(e)), 500

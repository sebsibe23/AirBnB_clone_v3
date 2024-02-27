#!/usr/bin/python3
''' Use Blueprint instance '''
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
    ''' returns status code'''
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def obj_count():
    ''' return count of objects '''
    amenity = storage.count(Amenity)
    city = storage.count(City)
    place = storage.count(Place)
    review = storage.count(Review)
    state = storage.count(State)
    user = storage.count(User)
    object_dict = {'amenities': amenity, 'cities': city, 'places': place,
                   'reviews': review, 'states': state, 'users': user}
    return jsonify(object_dict)

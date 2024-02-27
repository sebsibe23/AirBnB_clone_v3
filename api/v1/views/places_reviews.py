'''view for Review objects that handles
all default RESTFul API actions'''

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_reviews(place_id):
    ''' get and post review object '''
    if request.method == 'GET':
        place_obj = storage.get(Place, place_id)
        review_list = []
        if place_obj is None:
            abort(404)
        review_obj = getattr(place_obj, 'reviews')
        for review in review_obj:
            review_list.append(review.to_dict())
        return jsonify(review_list)

    if request.method == 'POST':
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.get_json()
            if 'user_id' not in body:
                abort(400, description='Missing user_id')
            user_obj = storage.get(User, body.get('user_id'))
            if user_obj is None:
                abort(404)
            if 'text' not in body:
                abort(400, description='Missing text')
            new_review = Review(**body)
            setattr(new_review, 'place_id', place_id)
            storage.new(new_review)
            storage.save()
            return make_response(jsonify(review.to_dict()), 201)
        else:
            abort(400, description='Not a JSON')


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def review_by_id(review_id):
    ''' get, delete, and put Review objects '''
    if request.method == 'GET':
        review_obj = storage.get(Review, review_id)
        if review_obj is None:
            abort(404)
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        review_obj = storage.get(Review, review_id)
        if review_obj is None:
            abort(404)
        storage.delete(review_obj)
        storage.save()
        return make_response({}, 200)

    if request.method == 'PUT':
        review_obj = storage.get(Review, review_id)
        if review_obj is None:
            abort(404)
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.get_json()
            banned_keys = ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']
            for key, value in body.items():
                if key not in banned_keys:
                    setattr(review_obj, key, value)
            storage.save()
            return make_response(jsonify(review_obj.to_dict()), 200)
        else:
            abort(400, description='Not a JSON')

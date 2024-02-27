#!/usr/bin/python3
'''view for User objects that handles all default RESTFul API actions'''

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_and_post_user():
    ''' get and post actions '''
    if request.method == 'GET':
        user_obj = storage.all(User)
        if user_obj is None:
            abort(404)
        user_list = []
        for value in user_obj.values():
            user_list.append(value.to_dict())
        return jsonify(user_list)

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.get_json()
            if 'email' not in body:
                abort(400, description='Missing email')
            elif 'password' not in body:
                abort(400, description='Missing password')
            else:
                new_user = User(**body)
                storage.new(new_user)
                storage.save()
                return make_response(jsonify(new_user.to_dict()), 201)
        else:
            abort(400, description='Not a JSON')


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_del_post_user(user_id):
    ''' get, delete, post actions with id provided '''
    if request.method == 'GET':
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404)
        return jsonify(user_obj.to_dict())

    if request.method == 'DELETE':
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404)
        storage.delete(user_obj)
        storage.save()
        return make_response({}, 200)

    if request.method == 'PUT':
        user_obj = storage.get(User, user_id)
        if user_obj is None:
            abort(404)
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.get_json()
            banned_keys = ['id', 'email', 'created_at', 'updated_at']
            for key, value in body.items():
                if key not in banned_keys:
                    setattr(user_obj, key, value)
            storage.save()
            return make_response(jsonify(user_obj.to_dict()), 200)
        else:
            abort(400, description='Not a JSON')

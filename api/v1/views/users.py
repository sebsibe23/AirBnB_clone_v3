#!/usr/bin/python3
<<<<<<< HEAD
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects.
    """
    try:
        users = storage.all(User).values()
        user_list = [user.to_dict() for user in users]
        return jsonify(user_list)
    except Exception:
        abort(500)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object based on user_id.
    """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
    except Exception:
        abort(500)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object based on user_id.
    """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500)


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Creates a new User object.
    """
    try:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        user = User(**data)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
    except Exception:
        abort(500)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object based on user_id.
    """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    except Exception:
        abort(500)
=======
'''
View for User objects that handles all default RESTFul API actions
'''
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_and_post_user():
    '''
    Handles GET and POST actions for users
    '''
    try:
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
    except Exception as e:
        return jsonify(error=str(e)), 500


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_del_post_user(user_id):
    '''
    Handles GET, DELETE, and PUT actions with provided user_id
    '''
    try:
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
    except Exception as e:
        return jsonify(error=str(e)), 500
>>>>>>> b1517d9e5a4c2f5a7b9821ce59e9d28b4cf8e5a1

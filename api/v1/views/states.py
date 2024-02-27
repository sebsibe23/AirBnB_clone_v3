#!/usr/bin/python3
'''view for State objects that handles all default RESTFUL API actions'''

from models.state import State
from models import storage
from flask import abort, make_response, jsonify, request
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    ''' manages state request '''
    if request.method == 'GET':
        all_state_object = storage.all(State)
        state_list = []
        for values in all_state_object.values():
            if storage.count(State) > 1:
                state_list.append(values.to_dict())
            else:
                return jsonify(values.to_dict())
        return jsonify(state_list)

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            body = request.get_json()
            if "name" not in body:
                abort(400, description='Missing name')
            else:
                new_state = State(**body)
                storage.new(new_state)
                storage.save()
                return make_response(jsonify(new_state.to_dict()), 201)
        else:
            abort(400, description='Not a JSON')


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    ''' handles all methods requests wit state_id '''
    if request.method == 'GET':
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404)
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404)
        storage.delete(state_obj)
        storage.save()
        return make_response({}, 200)

    if request.method == 'PUT':
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404)
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.get_json()
            for key, value in body.items():
                if key != 'id' or key != 'created_at' or key != 'updated_at':
                    setattr(state_obj, key, value)
            storage.save()
            return make_response(jsonify(state_obj.to_dict()), 200)
        else:
            abort(400, description='Not a JSON')

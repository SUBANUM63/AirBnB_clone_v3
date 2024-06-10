#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves all State objects
    :return: json of all states
    """
    states = storage.all("State").values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    create state route
    :return: newly created state obj
    """
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    kwargs = request.get_json()
    if kwargs:
        return abort(400, 'Not a JSON')
    if "name" not in kwargs:
        abort(400, 'Missing name')
    new_state = State(**kwargs)
    new_state.save()
    return jsonify(new_state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """
    gets a specific State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    return abort(404)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    updates specific State object by ID
    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get("State", state_id)

    if state:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        for key, val in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, val)
        state.save()
        return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found
    """
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

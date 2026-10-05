"""Run with python app.py; local development API on port 5000."""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from database import (FIELDS, create_db_table, insert_user, get_users,
                      get_user_by_id, update_user, delete_user)

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})
create_db_table()


def validated_user(require_id=False):
    user = request.get_json()
    if not isinstance(user, dict):
        return None, 'Request body must be a JSON object'
    for field in FIELDS:
        if not isinstance(user.get(field), str) or not user[field].strip():
            return None, f'{field} must be a non-empty string'
    if require_id and (type(user.get('user_id')) is not int or user['user_id'] <= 0):
        return None, 'user_id must be a positive integer'
    return user, None


@app.errorhandler(HTTPException)
def http_error(error):
    return jsonify(error=error.description), error.code


@app.get('/api/users')
def api_get_users():
    return jsonify(get_users())


@app.get('/api/users/<int:user_id>')
def api_get_user(user_id):
    user = get_user_by_id(user_id)
    return jsonify(user) if user else (jsonify(error='User not found'), 404)


@app.post('/api/users/add')
def api_add_user():
    user, error = validated_user()
    if error:
        return jsonify(error=error), 400
    return jsonify(insert_user(user)), 201


@app.put('/api/users/update')
def api_update_user():
    user, error = validated_user(require_id=True)
    if error:
        return jsonify(error=error), 400
    updated = update_user(user)
    return jsonify(updated) if updated else (jsonify(error='User not found'), 404)


@app.delete('/api/users/delete/<int:user_id>')
def api_delete_user(user_id):
    if not delete_user(user_id):
        return jsonify(error='User not found'), 404
    return jsonify(status='User deleted successfully')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', '5000')))

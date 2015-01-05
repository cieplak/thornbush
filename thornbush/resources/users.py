from __future__ import unicode_literals

from flask import jsonify, request

from thornbush import models
from thornbush.models.users import UserNameTaken, UserNotFound

from . import app, requires_auth, Resource



@app.route('/users', methods=['POST'])
@requires_auth
def create_user():
    payload = request.json
    name = payload.get('name')
    user, key = models.User.create(name=name)
    models.Session.commit()
    response_body = dict(
        id=user.guid,
        name=user.name,
        key=key,
        )
    return Resource.render(response_body), 201


@app.errorhandler(UserNameTaken)
def user_name_taken(error):
    response = jsonify(dict(message='User name is already taken'))
    response.status_code = 400
    return response

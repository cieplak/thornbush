from __future__ import unicode_literals
from functools import wraps
import json

from flask import Response, request

from thornbush import models

from thornbush.app import app


app_index = {

}


def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        request.user = models.User.lookup(auth.username)
        if not request.user.authenticate(auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@requires_auth
def root():
    return str(app_index)


class Resource(object):

    @classmethod
    def render(cls, obj):
        return json.dumps(obj, default=lambda x: str(x))


from comments import create_comment
from users import create_user, user_name_taken

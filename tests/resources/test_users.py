from __future__ import unicode_literals
import json

from thornbush import models
from thornbush.app import app


user = 'user'
password = 'password'


def setup_function(function):
    models.User.create(name=user, password=password)
    models.Session.commit()


def teardown_function(function):
    models.User.query.delete()
    models.Session.commit()


def test_create():
    client = app.test_client()

    credentials = '{}:{}'.format(user, password).encode('base64')
    headers = [
        ('Authorization', 'Basic {}'.format(credentials))
    ]
    user_definition = {
        'name': 'user2'
    }
    payload = json.dumps(user_definition)
    response = client.post(
        '/users', payload, headers=headers, data=payload,
        content_type='application/json'
    )
    expected_keys = ['id', 'name', 'key']
    for key in expected_keys:
        assert key in response.data

    # assert user name taken
    response2 = client.post(
        '/users', payload, headers=headers, data=payload,
        content_type='application/json'
    )
    assert response2.status_code == 400

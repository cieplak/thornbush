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
    models.Comment.query.delete()
    models.User.query.delete()
    models.Session.commit()


def test_create():
    client = app.test_client()
    credentials = '{}:{}'.format(user, password).encode('base64')
    headers = [
        ('Authorization', 'Basic {}'.format(credentials))
    ]
    comment = {
        'comment': 'this is a comment'
    }
    payload = json.dumps(comment)
    response = client.post(
        '/comments', payload, headers=headers, data=payload,
        content_type='application/json'
    )
    expected_keys = ['id', 'comment']
    for key in expected_keys:
        assert key in response.data


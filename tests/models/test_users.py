from __future__ import  unicode_literals
from datetime import datetime

from thornbush.models import Session, User


def teardown_function(function):
    Session.rollback()


def test_create_user():
    name = 'user'
    user, key = User.create(name=name)
    assert user.guid
    assert user.name == name


def test_delete_user():
    start_time = datetime.utcnow()
    user, key = User.create(name='user')
    user.delete()
    assert user.deleted_at > start_time

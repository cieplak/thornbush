from __future__ import  unicode_literals
from datetime import datetime

from thornbush.models import Session, Comment, User


def teardown_function(function):
    Session.rollback()


def test_create_comment():
    user, _ = User.create('user')
    comment = Comment.create(text='', user=user)
    assert comment.guid


def test_hierarchy():
    user, _ = User.create('user')
    parent = Comment.create(text='controversial comment', user=user)
    assert parent.guid
    user2, _ = User.create('user2')
    user3, _ = User.create('user3')
    child1 = user2.comment('insult', on=parent)
    child2 = user3.comment('insightful comment', on=parent)
    assert list(parent.descendents) == [child1, child2]
    assert list(child1.siblings) == [child2]
    assert list(child2.siblings) == [child1]
    assert child1.parent == parent
    assert child2.parent == parent


def test_delete_comment():
    user, _ = User.create('user')
    start_time = datetime.utcnow()
    comment = Comment.create(
        text='XML has superior schema validation',
        user=user,
    )
    comment.delete()
    assert comment.deleted_at > start_time


def test_create_comment_under_parent():
    user, _ = User.create('user')
    start_time = datetime.utcnow()
    comment = Comment.create(
        text='XML has superior schema validation',
        user=user,
    )
    Session.flush()
    comment.delete()
    assert comment.deleted_at > start_time

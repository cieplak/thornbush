from __future__ import unicode_literals
from datetime import datetime

import hashlib

from sqlalchemy import Column, DateTime, Table, Unicode
from sqlalchemy.orm.exc import NoResultFound

from thornbush import settings
from thornbush.lib import base62
from thornbush.models import Comment

from . import Base, Session


class UserNameTaken(Exception):
    pass


class UserNotFound(Exception):
    pass


users = Table(
    'users', Base.metadata,
    Column('guid', Unicode, primary_key=True,
                  default=lambda: 'US{}'.format(base62.guid())),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow),
    Column('deleted_at', DateTime),
    Column('name', Unicode, index=True),
    Column('key_hash', Unicode, nullable=False),
)


class User(Base):

    __tablename__ = 'users'

    @classmethod
    def create(cls, name, password=None):
        if cls.query.filter(cls.name == name).count():
            raise UserNameTaken()
        key = password or cls.generate_secret_key()
        key_hash = cls.hash(key)
        kwargs = dict(name=name, key_hash=key_hash)
        user = cls(**kwargs)
        Session.add(user)
        Session.flush()
        return user, key

    def comment(self, text, on=None):
        return Comment.create(text, user=self, parent=on)

    @classmethod
    def hash(cls, key):
        salt = settings.SECRET_SALT
        return hashlib.sha256(key + salt).hexdigest()

    @classmethod
    def generate_secret_key(cls):
        return 'secret_{}'.format(base62.guid())

    def delete(self):
        self.deleted_at = datetime.utcnow()
        Session.flush()
        return True

    def authenticate(self, password):
        return self.hash(password) == self.key_hash

    @classmethod
    def lookup(cls, name):
        query = User.query.filter(User.name == name)
        try:
            return query.one()
        except NoResultFound:
            raise UserNotFound()

from __future__ import unicode_literals
from collections import defaultdict
from datetime import datetime

from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, Table, Unicode, create_engine
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from thornbush.lib import base62
from . import Base, Session


comments = Table(
    'comments', Base.metadata,
    Column('guid', Unicode, primary_key=True,
           default=lambda: 'CM{}'.format(base62.guid())),
    Column('user_guid', Unicode, ForeignKey('users.guid'), index=True),

    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow),
    Column('deleted_at', DateTime),

    Column('texts', ARRAY(Unicode)),
    Column('version', Integer),

    Column('path', Unicode, index=True),
    Column('depth', Integer, default=0, index=True),
)


class Comment(Base):

    __tablename__ = 'comments'

    user = relationship('User')

    @classmethod
    def create(cls, text, user, parent=None):
        kwargs = dict(
            texts=[text],
            user=user,
        )
        comment = cls(**kwargs)
        Session.add(comment)
        Session.flush()
        if parent:
            comment.depth = parent.depth + 1
            comment.path = '/'.join([parent.path, comment.guid])
        else:
            comment.path = comment.guid
        Session.flush()
        return comment

    def update(self, text):
        self.version += 1
        self.texts.append(text)
        Session.flush()
        return self

    def delete(self):
        self.deleted_at = datetime.utcnow()
        Session.flush()
        return True

    @property
    def text(self):
        return self.texts[-1]

    @property
    def parent(self):
        if self.depth == 0:
            return
        parent_guid = self.path.split('/')[-2]
        parent = Comment.query.get(parent_guid)
        return parent

    @property
    def siblings(self):
        if self.depth == 0:
            return
        parent_path = self.path.replace(self.guid, '')
        query = (
            Comment.query
            .filter(Comment.path.like('{}%'.format(parent_path)))
            .filter(Comment.depth == self.depth)
            .filter(Comment.guid != self.guid)
        )
        return query

    @property
    def descendents(self):
        query = (
            Comment.query
            .filter(Comment.path.like('{}%'.format(self.path)))
            .filter(Comment.depth > self.depth)
        )
        return query

    @property
    def descendents_by_generation(self):
        generations = defaultdict(list)
        for node in self.descendents:
            generations[node.depth].append(node)
        return generations.values()

    @property
    def tree(self):
        return CommentTree(self)


class CommentTree(object):

    def __init__(self, root):
        self.root = root

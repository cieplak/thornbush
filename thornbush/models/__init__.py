from __future__ import unicode_literals

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from thornbush import settings

engine = create_engine(settings.DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = Session.query_property()


def db_init():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    User.create(name='root', password=settings.DEFAULT_ROOT_API_KEY)
    Session.commit()


from .comments import Comment
from .users import User

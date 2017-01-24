from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import urlzip.models  # noqa
    engine = db_session.connection().engine
    Base.metadata.create_all(bind=engine)


def drop_db():
    import urlzip.models  # noqa
    engine = db_session.connection().engine
    Base.metadata.drop_all(bind=engine)

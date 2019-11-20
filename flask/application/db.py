from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


@contextmanager
def session_scope():
    # cf.: https://copdips.com/2019/05/using-python-sqlalchemy-session-in-multithreading.html#way-2---using-scoped_session-to-create-a-thread-local-variable
    """Provide a transactional scope around a series of operations."""
    session = db.create_scoped_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

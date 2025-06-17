from contextlib import contextmanager
from database.sqlalchemy_config import db_config

@contextmanager
def get_db_session():
    """Context manager para sessões do banco"""
    session = db_config.get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Uso:
# with get_db_session() as session:
#     user = session.query(User).first()
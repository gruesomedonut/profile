from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config import config

db_engine = create_engine(config.RDS_URI, pool_pre_ping=True)
db_session_maker = sessionmaker(bind=db_engine)


@contextmanager
def acquire_db_session() -> Generator:
    session = db_session_maker()
    session.begin()
    try:
        yield session
        session.commit()
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()

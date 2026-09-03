# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base
from backend.models import (  # noqa: F401
    case,
    flag,
    known_entity,
    past_case,
    transaction,
    wallet_trail,
)


@pytest.fixture()
def db_session():
    """
    Creates a fresh in-memory SQLite database for each test function,
    so tests never touch your real chakravyuh.db file.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

import time
from pathlib import Path

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.sql import delete, insert, select, text
from sqlalchemy.orm import sessionmaker, clear_mappers

import request.config as config
from request.entrypoints.flask_app import create_app
from request.domain.model import Assigned
from request.adapters.orm import mapper_registry, start_mappers, assignments

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture
def in_memory_db():
    engine = create_engine(f"sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def file_sqlite_db():
    engine = create_engine(config.get_sqlite_filedb_uri())
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(file_sqlite_db):
    start_mappers()
    yield sessionmaker(bind=file_sqlite_db)()
    clear_mappers()


@pytest.fixture
def postgres_session_factory(postgres_db):
    yield sessionmaker(bind=postgres_db)


@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()

@pytest.fixture
def flask_api(session):
    app = create_app()
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def test_client(flask_api):
    return flask_api.test_client()

@pytest.fixture
def add_assigned(session):
    # take care and note that this fixture takes care of adding in records to the database.
    assignments_added = set()
    requests_added = set()

    def _add_assigned(assigned):
        #print(assigned)
        for id, request_id, approval_id, vehicle_id, app_date, notes in assigned:
            session.execute(
                insert(assignments).values(
                    id=id, request_id=request_id, approval_id=approval_id, vehicle_id=vehicle_id, app_date=app_date, notes=notes
                )
            )
            assign_id = session.scalars(
                select(Assigned).where(Assigned.id == id).where(Assigned.request_id == request_id)
            ).first()
            #print(assign_id.id)
            #print(assign_id.request_id)
            assignments_added.add(assign_id.id)
            requests_added.add(assign_id.request_id)
        session.commit()
        session.close()

    yield _add_assigned

    for assign_id in assignments_added:
        session.execute(
            text("DELETE FROM assignments WHERE id=:assign_id"),
            dict(assign_id=assign_id),
        )
    
    session.commit()

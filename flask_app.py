from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

import config
import model
import orm
import repository
import services


def index_endpoint():
    return "<p>HELLO FROM THE API</p>"


def assign_endpoint():
    clear_mappers()
    orm.start_mappers()
    get_session = sessionmaker(bind=create_engine(config.get_sqlite_filedb_uri()))
    session = get_session()
    repo = repository.SqlAlchemyRequestRepository(session)
    vehicle = model.Vehicle(
        request.json["id"],
        request.json["name"],
        request.json["notes"],
    )

    try:
        batchref = services.allocate(vehicle, repo, session)
    except (model.VehicleInUse, services.InvalidVehicle) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201


def create_app():
    app = Flask(__name__)
    app.config.update({"TESTING": True})

    app.add_url_rule("/", "index", view_func=index_endpoint)
    app.add_url_rule(
        "/allocate", "allocate", view_func=allocate_endpoint, methods=["POST"]
    )

    return app

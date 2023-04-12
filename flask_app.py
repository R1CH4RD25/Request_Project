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


def assignments_endpoint():
    clear_mappers()
    orm.start_mappers()
    get_session = sessionmaker(bind=create_engine(config.get_sqlite_filedb_uri()))
    session = get_session()
    repo = repository.SqlAlchemyAssignedRepository(session)
    requests = model.Request(
        request.json["id"],
        request.json["requestor"],
        request.json["activity"],
        request.json["destination"],
        request.json["vehicle_id"],
        request.json["req_date"],
        request.json["req_time"],
    )

    if requests.vehicle_id == 100:
        approval = model.Approval(1007, "Approved", 101, requests.id, "Drive Safe")
    else:
        requests.vehicle_id = 100
        approval = model.Approval(1007, "Approved", 100, requests.id, "Drive Safe")
    
    try:
        assignid = services.assign(requests, approval, repo, session)

        if assignid != False:
            return {"assignid": assignid}, 201
        else:
             return {"message": "Error - Cannot Assign Vehicle"}, 400
    except (model.VehicleInUse, services.InvalidVehicle) as e:
        return {"message": str(e)}, 400

    


def create_app():
    app = Flask(__name__)
    app.config.update({"TESTING": True})

    app.add_url_rule("/", "index", view_func=index_endpoint)
    app.add_url_rule(
        "/assignments", "assignments", view_func=assignments_endpoint, methods=["POST"]
    )

    return app

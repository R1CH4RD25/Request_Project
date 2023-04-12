from __future__ import annotations

import request.domain.model as model
from request.domain.model import Vehicle
from request.adapters.repository import AbstractAssignedRepository, SqlAlchemyAssignedRepository


class InvalidVehicle(Exception):
    pass


def is_valid_vehicle(id, vehicles):
    return id in {v.id for v in vehicles}


def assign(request, approval, repo: AbstractAssignedRepository, session) -> str:
    assignments = [
        model.Assigned(9997, 1004, 1006, 101, "2011-01-02", ""),
        model.Assigned(9998, 1005, 1007, 100, "2011-01-02", ""),
        model.Assigned(9999, 1003, 1008, 102, "03/30/2023", ""),
    ]
    assignment = repo.list()
    #print(request)
    #print(approval)
    #print(assignments[1].vehicle_id)
    #Need assistance with mappers and properties
    #assignments = repo.list()
    assignid = model.assign(request,approval, assignment)
    #print(request.id, assignid)
    session.commit()
    return assignid
   

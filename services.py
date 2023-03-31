from __future__ import annotations

import model
from model import Vehicle
from repository import AbstractRequestRepository


class InvalidVehicle(Exception):
    pass


def is_valid_vehicle(id, vehicles):
    return id in {v.id for v in vehicles}




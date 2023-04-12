import random
import pytest
import requests
import request.config as config

from datetime import datetime

def random_id():
    return random.randint(1000,9999)


def test_api_works(test_client):
    url = config.get_api_url()
    r = test_client.get(f"{url}/")
    assert r.status_code == 200
    assert b"HELLO FROM THE API" in r.data


def test_unhappy_path_returns_400_and_error_message(add_assigned, test_client):
    firstid, otherid = random_id(), random_id()
    #print(firstid)
    earlyassign = random_id()
    laterassign = random_id()
    otherassign = random_id()
    add_assigned(
        [
            (laterassign, firstid, 1005, 100, "2011-01-02", None),
            (earlyassign, firstid, 1006, 100, "2011-01-02", None),
            (otherassign, otherid, 1007, 100, "2011-01-02", None),
        ]
    )
    data = {"id": earlyassign, "requestor": "Christy Eli", "activity": "Golf", "destination": "Graham", "vehicle_id": 100, "req_date": "2011-01-02", "req_time": "10:00 AM"}
    url = config.get_api_url()
    
    r = test_client.post(f"{url}/assignments", json=data)

    
    assert r.status_code == 400
    assert r.json["message"] == "Error - Cannot Assign Vehicle"


def test_happy_path_returns_201_and_assigned_vehicle(add_assigned, test_client):
    firstid, otherid = random_id(), random_id()
    #print(firstid)
    earlyassign = random_id()
    laterassign = random_id()
    otherassign = random_id()
    add_assigned(
        [
            (laterassign, firstid, 1005, 100, "2011-01-02", None),
            (earlyassign, firstid, 1006, 100, "2011-01-02", None),
            (otherassign, otherid, 1007, 100, "2011-01-02", None),
        ]
    )

    data = {"id": firstid, "requestor": "Christy Eli", "activity": "Golf", "destination": "Graham", "vehicle_id": 101, "req_date":datetime.strptime("2011-01-02", "%Y-%m-%d"), "req_time": "10:00 AM"}
    url = config.get_api_url()
    r = test_client.post(f"{url}/assignments", json=data)

    assert r.status_code == 201

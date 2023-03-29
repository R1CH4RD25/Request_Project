from datetime import datetime
from dataclasses import dataclass


@dataclass()
class Vehicle:
    id: int
    name: str
    notes: str

@dataclass()
class Request:
    id: int
    requestor: str
    activity: str
    destination: str
    vehicle_id: int
    req_date: datetime
    req_time: datetime

@dataclass()
class Approval:
     id: int
     status: str
     vehicle_id: int
     request_id: int
     notes: str
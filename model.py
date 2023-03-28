from datetime import datetime
from dataclasses import dataclass

class Vehicle:
    
    def __init__(self, id: int, name: str, notes: str):
        self.id = id
        self.name = name
        self.notes = notes
    '''
    id: int
    name: str
    notes: str
'''
    def __iter__(self):
        return iter((self.id, self.name, self.notes))


class Request:
     def __init__(self, id: int, requestor: str, activity: str, destination: str,
                  vehicle_id: int, req_date: datetime, req_time: datetime) -> None:
        self.id = id
        self.requestor = requestor
        self.activity = activity
        self.destination = destination
        self.vehicle_id = vehicle_id
        self.req_date = req_date
        self.req_time = req_time

class Approval:
     def __init__(self, id: int, status: str, vehicle_id: int, request_id: int,
                  notes: str) -> None:
        self.id = id
        self.status = status
        self.vehicle_id = vehicle_id
        self.request_id = request_id
        self.notes = notes
from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Set

class VehicleInUse(Exception):
    pass


def assign(request: Request, approval: Approval, assignments: List[Assigned]) -> str:

    try:
        for assign in assignments:
            #print(assign.assign(request, approval))
            #print(approval.vehicle_id, assign.vehicle_id)            
            #print(approval.request_id, request.id)
            #print(request.req_date, assign.app_date)
            if assign.assign(request, approval) == False:
                return False
        return assign.id + 1
    except StopIteration:
        return False
       

@dataclass(unsafe_hash=True)
class Vehicle:
    id: int
    name: str
    notes: str

@dataclass(unsafe_hash=True)
class Request:
    id: int
    requestor: str
    activity: str
    destination: str
    vehicle_id: int
    req_date: datetime
    req_time: datetime
  
@dataclass(unsafe_hash=True)
class Approval:
     id: int
     status: str
     vehicle_id: int
     request_id: int
     notes: str


#@dataclass()
class Assigned:
    def __init__(self, id: int, request_id: int, approval_id: int, vehicle_id: int, app_date: datetime, notes: Optional[str]):
        self.id = id
        self.request_id = request_id
        self.approval_id = approval_id
        self.vehicle_id = vehicle_id
        self.app_date = app_date
        self.notes = notes       
        self._assignments = set()

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other): 
        if not isinstance(other, Assigned):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.request_id == other.request_id
    
    def assign(self, request: Request, approval: Approval):
        if self.can_assign(request, approval) == True:
            print(request)
            self._assignments.add(request)
        else:  
            return False

    def can_assign(self, request:Request, approval:Approval) -> bool:
        return approval.request_id == request.id and self.app_date != request.req_date or self.vehicle_id != approval.vehicle_id
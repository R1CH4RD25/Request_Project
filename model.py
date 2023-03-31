from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Set

class VehicleInUse(Exception):
    pass


def assign(request: Request, approval: Approval, assignments: List[Assigned]) -> str:
    try:
        assign = next(b for b in assignments if b.can_assign(request, approval))
        print(assign)
        assign.assign(request, approval)
        return assign.id
    except StopIteration:
        raise VehicleInUse(f"Out of stock for sku {approval.vehicle_id}")

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
        if self.can_assign(request, approval):
            self._assignments.add()

    def can_assign(self, request:Request, approval:Approval) -> bool:
        return self.app_date != request.req_date or self.vehicle_id != approval.vehicle_id
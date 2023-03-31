from datetime import date

import model



def make_requests(req_id, veh_id, ddate):
    return(
        model.Request(req_id, "Christy Eli", "UIL Event", "Graford, TX", veh_id, ddate, "8:00 PM"),
        model.Approval(1007, "Approved", veh_id, req_id, "Drive Safe"),
    )


def test_can_vehicle_be_assigned():
    #Create preassigned
    assigned = model.Assigned(9999, 1004, 1007, 101, "03/28/2023", "")

    make_requests(1005, 100, "05/01/2023")
    request, approval = make_requests(1004, 101, "03/28/2023")

    assert assigned.can_assign(request, approval) != True

def test_returns_assigned_id():
    assign1 = model.Assigned(9997, 1004, 1006, 101, "03/28/2023", "")
    assign2 = model.Assigned(9998, 1005, 1007, 100, "03/29/2023", "")
    assign3 = model.Assigned(9999, 1003, 1008, 102, "03/30/2023", "")
    
    request = model.Request(1004, "Christy Eli", "UIL Event", "Graford, TX", 101, "03/29/2023", "8:00 PM")
    approval = model.Approval(1007, "Approved", 1001, 1004, "Drive Safe")

        
    alloc = model.assign(request,approval, [assign1, assign2, assign3])  

    print(alloc)
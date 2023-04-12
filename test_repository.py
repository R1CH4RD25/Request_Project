# pylint: disable=protected-access
import model
import repository

from sqlalchemy import select, delete
from sqlalchemy.sql import text


def test_repository_can_save_a_request(session):
    # delete all records first
    session.execute(delete(model.Request))
    request = model.Request(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM")
    

    repo = repository.SqlAlchemyRequestRepository(session)
    repo.add(request)
    session.commit()

    rows = session.execute(
        text('SELECT id,  requestor, activity, destination, vehicle_id, req_date, req_time FROM "requests"')
    )
    assert list(rows) == [(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM")]

    session.commit()


def insert_request(session):
    session.execute(
        text(
            "INSERT INTO requests (id, requestor, activity, destination, vehicle_id, req_date, req_time) VALUES "
            '(1004, "Christy Eli", "UIL Event", "Graford, TX", 101, "03/29/2023", "8:00 PM")'
        )
    )
    [[request_id]] = session.execute(
        text("SELECT id FROM requests WHERE id=:id AND requestor=:requestor"),
        dict(id=1004, requestor="Christy Eli"),
    )
    return request_id

def insert_approval(session, approval_id, request_id):
    session.execute(
        text(
            "INSERT INTO approvals (id, status, vehicle_id, request_id, notes) VALUES"
            '(:approval_id, "Approved", 1001, 1004, "Drive Safe")'
        ),
        dict(approval_id=approval_id),
    )
    [[approval_id]] = session.execute(
        text("SELECT id FROM approvals WHERE id=:approval_id AND request_id=:request_id"),
        dict(approval_id=approval_id, request_id=1004),
    )
    return approval_id

def new_id(session):
    #Calculate the next ID in the list
    last_id = session.scalars(select(model.Approval)).all()
    return last_id[-1].id + 1
    


def test_repository_can_retrieve_request_with_approval(session):
    session.execute(delete(model.Request))
    session.execute(delete(model.Approval))

    #Insert Desired Request
    request_id = insert_request(session)

    #Insert fake approvals
    insert_approval(session, 1004, 1009)    
    insert_approval(session, new_id(session), 1010)

    #Insert approval we wish to find
    approval_id = insert_approval(session, new_id(session), request_id)
    
    #Retrieve approval from Repo
    apprepo = repository.SqlAlchemyApprovalRepository(session)
    appretrieved = apprepo.get(approval_id)

    #Retrieve Request from Repo using approval repo
    reqrepo = repository.SqlAlchemyRequestRepository(session)
    reqretrieved = reqrepo.get(appretrieved.request_id)

    expected = model.Request(1004, "Christy Eli", "UIL Event", "Graford, TX", 101, "03/29/2023", "8:00 PM")

    session.commit()
    
    assert expected == reqretrieved
    assert appretrieved.request_id == reqretrieved.id


def test_repository_can_save_an_assignment(session):
    # delete all records first
    session.execute(delete(model.Assigned))
    assigned = model.Assigned(5000, 1005, 2550, 102, "04/06/2023", "Notes")
    

    repo = repository.SqlAlchemyAssignedRepository(session)
    repo.add(assigned)
    session.commit()

    rows = session.execute(
        text('SELECT id,  request_id, approval_id, vehicle_id, app_date, notes FROM "assignments"')
    )
    assert list(rows) == [(5000, 1005, 2550, 102, "04/06/2023", "Notes")]

    session.commit()
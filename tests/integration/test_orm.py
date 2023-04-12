import request.domain.model as model
import request.adapters.orm as orm
import pickle
from datetime import date
from sqlalchemy import select, delete, insert
from sqlalchemy.sql import text



def test_vehicles_mapper_can_load_lines(session):
    # delete all records first
    session.execute(delete(model.Vehicle))

    session.execute(
        text(
            "INSERT INTO vehicles (id, name, notes) VALUES "
            '(1001, "Victory Machine", ""),'
            '(1002, "Suburban 01", ""),'
            '(1003, "Van 01", "")'
        )
    )

    outcome = session.scalars(select(model.Vehicle)).all()    

    expected = [
        model.Vehicle(1001, "Victory Machine", ""),
        model.Vehicle(1002, "Suburban 01", ""),
        model.Vehicle(1003, "Van 01", ""),
    ]

    assert outcome == expected
    session.close()

def test_vehicles_mapper_can_save_lines(session):
    # delete all records first
    session.execute(delete(model.Vehicle))

    new_line = model.Vehicle(1001, "Victory Machine", "")
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT id, name, notes FROM "vehicles"')))
    assert rows == [(1001, "Victory Machine", "")]

    session.close()



def test_requests_mapper_can_load_lines(session):
    # delete all records first
    session.execute(delete(model.Request))

    session.execute(
        text(
            "INSERT INTO requests (id, requestor, activity, destination, vehicle_id, req_date, req_time) VALUES "
            '(1004, "Christy Eli", "UIL Event", "Graford, TX", 101, "03/29/2023", "8:00 PM"),'
            '(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM"),'
            '(1006, "Shane Mallory", "District Track", "Bryson, TX", 101, "04/09/2023", "7:00 AM")'
        )
    )

    outcome = session.scalars(select(model.Request)).all()    

    expected = [
        model.Request(1004, "Christy Eli", "UIL Event", "Graford, TX", 101, "03/29/2023", "8:00 PM"),
        model.Request(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM"),
        model.Request(1006, "Shane Mallory", "District Track", "Bryson, TX", 101, "04/09/2023", "7:00 AM"),
    ]

    assert outcome == expected
    session.close()


def test_requests_mapper_can_save_lines(session):
    # delete all records first
    session.execute(delete(model.Request))

    new_line = model.Request(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM")
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT id, requestor, activity, destination, vehicle_id, req_date, req_time FROM "requests"')))
    assert rows == [(1005, "Richard Sullivan", "Golf", "Archer City", 102, "04/06/2023", "6:30 AM")]

    session.close()


def test_approvals_mapper_can_load_lines(session):
    # delete all records first
    session.execute(delete(model.Approval))

    session.execute(
        text(
            "INSERT INTO approvals (id, status, vehicle_id, request_id, notes) VALUES "
            '(1007, "Approved", 1001, 1004, "Drive Safe"),'
            '(1008, "Approved", 1002, 1005, "Might want to leave earlier"),'
            '(1009, "Denied", 1003, 1006, "Come see me")'
        )
    )

    outcome = session.scalars(select(model.Approval)).all()    

    expected = [
        model.Approval(1007, "Approved", 1001, 1004, "Drive Safe"),
        model.Approval(1008, "Approved", 1002, 1005, "Might want to leave earlier"),
        model.Approval(1009, "Denied", 1003, 1006, "Come see me"),
    ]

    assert outcome == expected
    session.close()


def test_approvals_mapper_can_save_lines(session):
    # delete all records first
    session.execute(delete(model.Approval))

    new_line = model.Approval(1007, "Approved", 1001, 1004, "Drive Safe")
    print(new_line)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT id, status, vehicle_id, request_id, notes FROM "approvals"')))
    assert rows == [(1007, "Approved", 1001, 1004, "Drive Safe")]

    session.close()


def test_retrieving_requests(session):
    # delete all records first
    session.execute(delete(model.Request))

    session.execute(
        text(
            "INSERT INTO requests (id, requestor, activity, destination, vehicle_id, req_date, req_time) VALUES "
            '(1004, "Christy Eli", "UIL Event", "Graford, TX", 101, "03/29/2023", "8:00 PM")'
        )
    )

    session.execute(
        text(
            "INSERT INTO requests (id, requestor, activity, destination, vehicle_id, req_date, req_time) VALUES "
            '(1006, "Shane Mallory", "District Track", "Bryson, TX", 101, "04/09/2023", "7:00 AM")'
        )
    )

    outcome = session.scalars(select(model.Request)).all()    

    expected = [
        model.Request(1004, "Christy Eli", "UIL Event", "Graford, TX", 101, "03/29/2023", "8:00 PM"),
        model.Request(1006, "Shane Mallory", "District Track", "Bryson, TX", 101, "04/09/2023", "7:00 AM"),
    ]

    assert outcome == expected
    session.close()



def test_assigned_mapper_can_load_lines(session):
    # delete all records first
    session.execute(delete(model.Assigned))

    session.execute(
        text(
            "INSERT INTO assignments (id, request_id, approval_id, vehicle_id, app_date, notes) VALUES "
            '(5007, 1007, 101, 1004, "03/25/2023", "Drive Safe"),'
            '(5008, 1008, 102, 1005, "03/28/2023", "")'
        )
    )
    
    outcome = session.scalars(select(model.Assigned)).all()    

    expected = [
        model.Assigned(5007, 1007, 101, 1004, "03/25/2023", "Drive Safe"),
        model.Assigned(5008, 1008, 102, 1005, "03/28/2023", ""),
    ]

    assert outcome == expected
    session.close()



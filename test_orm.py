import model
import orm
from datetime import date
from sqlalchemy import select, delete, insert
from sqlalchemy.sql import text



def test_vehicles_mapper_can_load_lines(session, in_memory_sqlite_db):
    # delete all records first
    with in_memory_sqlite_db.connect() as session:
        session.execute(delete(model.Vehicle))

        session.execute(
            text(
                "INSERT INTO vehicles (id, name, notes) VALUES "
                '(1001, "Victory Machine", ""),'
                '(1002, "Suburban 01", ""),'
                '(1003, "Van 01", "")'
            )
        )

        outcome = session.execute(select(model.Vehicle)).all()

    

    vehicle = model.Vehicle

    test = vehicle(1004,"Van 02","")

    expected = [
        model.Vehicle(1001, "Victory Machine", ""),
        model.Vehicle(1002, "Suburban 01", ""),
        model.Vehicle(1003, "Van 01", ""),
    ]
    
    print(test)
    print(outcome)
    print(expected)
    #assert outcome == expected
    session.close()

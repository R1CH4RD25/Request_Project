import pytest
from sqlalchemy.sql import delete, insert, select, text
from request.domain import model
from request.adapters.orm import allocations, requests
from request.service_layer import unit_of_work

def insert_request(session, id, requestor, activity, destination, vehicle_id, req_date,req_time):
    session.execute(
        insert(requests).values(id=id, requestor=requestor, activity=activity, destination=destination, vehicle_id=vehicle_id, req_date=req_date, req_time=req_time)

    )


def test_uow_can_retrieve_a_request_and_assign(session_factory):
    session = session_factory
    insert_request(session, "batch1", "HIPSTER-WORKBENCH", 100, None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        batch = uow.batches.get(reference="batch1")
        line = model.OrderLine("o1", "HIPSTER-WORKBENCH", 10)
        batch.allocate(line)
        uow.commit()

    batchref = get_allocated_batch_ref(session, "o1", "HIPSTER-WORKBENCH")
    assert batchref == "batch1"
    session.close()
from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

from typing import Text

import logging
import model

logger = logging.getLogger(__name__)

metadata = MetaData()

mapper_registry = registry()


vehicles = Table(
    "vehicles",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("notes", String()),
)

requests = Table(
    "requests",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("requestor", String(255)),
    Column("activity", String(255)),
    Column("destination", String(255)),
    Column("vehicle_id", ForeignKey("vehicles.id")),
    Column("req_date", Date),
    Column("req_time", Date),
)

approvals = Table(
    "approvals",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("status", String(255)),
    Column("vehicle_id", ForeignKey("vehicles.id")),
    Column("request_id", ForeignKey("requests.id")),
    Column("notes", String()),
)

def start_mappers():
    logger.info("string mappers")
    # SQLAlchemy 2.0
    vehicles_mapper = mapper_registry.map_imperatively(model.Vehicle, vehicles)
    #requests_mapper = mapper_registry.map_imperatively(model.Request, requests)
    #approvals_mapper = mapper_registry.map_imperatively(model.Approval, approvals)
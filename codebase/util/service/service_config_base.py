from model.core.objects.endpoint import DatabaseEndPoint
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from dataclasses import dataclass

from util.db import create_db_engine
from util.env import database_endpoint_from_env

@dataclass
class ServiceConfig:

    write_model_db_endpoint: DatabaseEndPoint
    read_model_db_endpoint: DatabaseEndPoint

    def write_model_db_engine(self) -> Engine:
        return create_db_engine(self.write_model_db_endpoint)

    def read_model_db_engine(self) -> Engine:
        return create_db_engine(self.read_model_db_endpoint)

    def write_model_db_session(self) -> Session:
        return Session(bind=self.write_model_db_engine())

    def read_model_db_session(self) -> Session:
        return Session(bind=self.read_model_db_engine())

def default_service_config() -> ServiceConfig:

    return ServiceConfig(
        write_model_db_endpoint=database_endpoint_from_env('WRITE_MODEL_DB'),
        read_model_db_endpoint=None
        # read_model_db_endpoint=database_endpoint_from_env('READ_MODEL_DB')
    )
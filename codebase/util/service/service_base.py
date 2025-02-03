from dataclasses import dataclass
import datetime
import traceback
from typing import Callable
from model.core.objects.logevent import (
    HealthChecked,
    RequestFailed,
    RequestReceivedLogEvent,
    ResponseReturnedLogEvent,
    ServiceStartupLogicExceptionOccurred,
    ServiceWebServeExceptionOccurred,
)
from services.migration.client import MigrationServiceClient
from util.service.service_config_base import ServiceConfig
from util.web import serialize_datetime
import uvicorn
from util.structured_logging import configure_structured_logging, configure_structured_logging
from model.core.objects.service import Service
from util.structured_logging import log_event
from util.env import env_int, env_str
from fastapi.exceptions import HTTPException
import uuid
from typing import Callable
from util.structured_logging import log_event
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@dataclass
class ServiceDefinition:
    service: Service
    config: ServiceConfig
    wait_for_migrations: bool = True
    before_launching_service: callable = None
    api: any = None


def register_healthcheck_endpoint(api):
    @api.get("/healthcheck")
    def get_root():
        log_event(HealthChecked(timestamp=serialize_datetime(datetime.datetime.now())))


def start_service(
    definition: ServiceDefinition,
):
    configure_structured_logging(definition.service)

    if definition.wait_for_migrations:
        MigrationServiceClient.wait_until_ready()

    if definition.before_launching_service:
        try:
            definition.before_launching_service(definition.config)
        except:
            log_event(ServiceStartupLogicExceptionOccurred(info=traceback.format_exc()))
            raise

    try:
        uvicorn.run(
            app=f"services.{definition.service.value}.service:api",
            factory=True,
            host=env_str("SERVICE_HOST"),
            port=env_int("SERVICE_PORT"),
            log_level="info",
            reload=True,
            reload_dirs=["/application"],
            reload_includes=["*.py"],
            reload_excludes=["*.log"],
            reload_delay=1,
        )
    except:
        log_event(ServiceWebServeExceptionOccurred(info=traceback.format_exc()))
        raise


def api_for_service_definition(definition: ServiceDefinition) -> FastAPI:
    api = FastAPI()
    configure_structured_logging(definition.service)
    register_healthcheck_endpoint(api)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Allows requests from your frontend port
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods
        allow_headers=["*"],  # Allows all headers
    )
    return api


def request_handler(service_definition: ServiceDefinition, TRqModel, callback: Callable):
    def handle(*args):
        rq = None
        if len(args) > 0:
            rq = args[0]

        rsp = None
        try:
            if TRqModel is None:
                if rq is None:
                    rsp = callback(service_definition.config)
                else:
                    rsp = callback(service_definition.config, rq)

                log_event(ResponseReturnedLogEvent(rsp_type=rsp.__class__.__name__, rsp=str(rsp)))

            else:
                log_event(RequestReceivedLogEvent(rq_type=TRqModel.__name__, rq=str(rq)))

                rsp = callback(service_definition.config, rq)

                log_event(ResponseReturnedLogEvent(rsp_type=rsp.__class__.__name__, rsp=str(rsp)))

            return rsp

        except:
            error_reference = uuid.uuid4()
            trace = traceback.format_exc()
            print(trace)
            log_event(
                RequestFailed(
                    request_type=TRqModel.__name__,
                    request=str(rq),
                    error=trace,
                    reference=str(error_reference),
                )
            )
            raise HTTPException(status_code=500, detail=f"reference {error_reference} - {trace}")

    return handle

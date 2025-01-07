from model.common import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config
from services.read_model_sync.logic import before_launching_read_model_sync_server


def read_model_sync_service_definition():
    return ServiceDefinition(
        service = Service.READ_MODEL_SYNC,
        config = default_service_config(),
        before_launching_service=before_launching_read_model_sync_server
    )
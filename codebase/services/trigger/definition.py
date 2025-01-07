from model.common import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config

def trigger_service_definition():
    return ServiceDefinition(
        service = Service.TRIGGER,
        config = default_service_config(),
    )
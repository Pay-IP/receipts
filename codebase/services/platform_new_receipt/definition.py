from model.common import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config

def platform_new_receipt_service_definition():
    return ServiceDefinition(
        service = Service.PLATFORM_NEW_RECEIPT,
        config = default_service_config(),
    )
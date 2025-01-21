from model.core.objects.service import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config

def platform_new_payment_service_definition():
    return ServiceDefinition(
        service = Service.PLATFORM_NEW_PMT,
        config = default_service_config(),
    )
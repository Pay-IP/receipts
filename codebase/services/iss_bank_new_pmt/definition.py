from model.common import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config

def issuing_bank_new_payment_service_definition():
    return ServiceDefinition(
        service = Service.ISS_BANK_NEW_PMT,
        config = default_service_config(),
    )
from model.object_model.core.service import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config

def payment_processor_new_payment_service_definition():
    return ServiceDefinition(
        service = Service.PMT_PROC_NEW_PMT,
        config = default_service_config(),
    )
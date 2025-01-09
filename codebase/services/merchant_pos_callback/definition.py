from model.object_model.core.service import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config

def merchant_pos_callback_service_definition():
    return ServiceDefinition(
        service = Service.MERCHANT_POS_CALLBACK,
        config = default_service_config(),
    )
from model.core.objects.service import Service
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config
from services.platform_matching.logic import before_launching_platform_matching_rest_server


def platform_matching_service_definition():
    return ServiceDefinition(
        service = Service.PLATFORM_MATCHING,
        config = default_service_config(),
        before_launching_service=before_launching_platform_matching_rest_server
    )
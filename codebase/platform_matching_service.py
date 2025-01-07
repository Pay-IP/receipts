


from services.platform_matching.definition import platform_matching_service_definition
from util.service.service_base import start_service
from model.common import Service

if __name__ == '__main__':
    start_service(
        definition=platform_matching_service_definition()
    )
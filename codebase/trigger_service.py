from util.service.service_base import start_service
from services.trigger.definition import trigger_service_definition

if __name__ == '__main__':
    start_service(
        definition=trigger_service_definition()
    )
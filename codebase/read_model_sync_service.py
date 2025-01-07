from services.read_model_sync.definition import read_model_sync_service_definition
from util.service.service_base import start_service
from model.common import Service

if __name__ == '__main__':
    start_service(
        definition=read_model_sync_service_definition(),
    )
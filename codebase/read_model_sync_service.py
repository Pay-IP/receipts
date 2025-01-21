from services.read_model_sync.definition import read_model_sync_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=read_model_sync_service_definition(),
    )
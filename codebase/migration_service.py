from services.migration.definition import migration_service_definition
from util.service.service_base import start_service

if __name__ == '__main__':
    start_service(
        definition=migration_service_definition()
    )
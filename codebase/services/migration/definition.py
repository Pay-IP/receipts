from model.core.objects.service import Service
from services.migration.logic import before_launching_migration_server
from util.service.service_base import ServiceDefinition
from util.service.service_config_base import default_service_config

def migration_service_definition():
    return ServiceDefinition(
        service = Service.MIGRATION,
        config = default_service_config(),
        wait_for_migrations=False,
        before_launching_service=before_launching_migration_server,
    )
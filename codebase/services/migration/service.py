from util.service.service_base import ServiceDefinition, api_for_service_definition
from services.migration.definition import migration_service_definition


def api():

    definition: ServiceDefinition = migration_service_definition()    
    api = api_for_service_definition(definition)
    
    return api
from util.service.service_base import ServiceDefinition, api_for_service_definition
from services.platform_matching.definition import platform_matching_service_definition

def api():

    definition: ServiceDefinition = platform_matching_service_definition()    
    api = api_for_service_definition(definition)
    return api
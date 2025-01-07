from util.service.service_base import ServiceDefinition, api_for_service_definition
from services.read_model_sync.definition import read_model_sync_service_definition

def api():

    definition: ServiceDefinition = read_model_sync_service_definition()    
    api = api_for_service_definition(definition)
    return api
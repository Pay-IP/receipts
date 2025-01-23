from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.trigger.logic import handle_trigger_random_merchant_pos_new_checkout_request
from services.trigger.definition import trigger_service_definition

def api():

    definition: ServiceDefinition = trigger_service_definition()    
    api = api_for_service_definition(definition)
    
    @api.post("/merchant_pos_new_checkout")
    def merchant_pos_new_checkout():
        return request_handler(
            definition,
            None, 
            handle_trigger_random_merchant_pos_new_checkout_request
        )()
        
    return api
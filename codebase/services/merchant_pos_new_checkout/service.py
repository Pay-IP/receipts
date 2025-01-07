from util.service.service_base import ServiceDefinition, api_for_service_definition
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest
from util.service.service_base import request_handler
from services.merchant_pos_new_checkout.logic import handle_merchant_pos_new_checkout_request
from services.merchant_pos_new_checkout.definition import merchant_pos_new_checkout_service_definition

def api():

    definition: ServiceDefinition = merchant_pos_new_checkout_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def checkout(rq: MerchantPosNewCheckoutRequest):
        return request_handler(
            definition,
            MerchantPosNewCheckoutRequest, 
            handle_merchant_pos_new_checkout_request
        )(rq)
    
    return api
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest
from util.service.service_base import ServiceDefinition, api_for_service_definition, request_handler
from services.platform_new_pmt.logic import handle_new_payment_request_to_platform_from_customer_bank
from services.platform_new_pmt.definition import platform_new_payment_service_definition

def api():

    definition: ServiceDefinition = platform_new_payment_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def new_payment(rq: PlatformNewPaymentRequest):
        return request_handler(
            definition,
            PlatformNewPaymentRequest, 
            handle_new_payment_request_to_platform_from_customer_bank
        )(rq)

    return api

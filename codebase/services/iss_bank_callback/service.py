from services.iss_bank_callback.rqrsp import IssuingBankCallbackRequest
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.iss_bank_callback.logic import handle_issuing_bank_callback_request
from services.iss_bank_callback.definition import issuing_bank_callback_service_definition

def api():

    definition: ServiceDefinition = issuing_bank_callback_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def callback(rq: IssuingBankCallbackRequest):
        return request_handler(
            definition,
            IssuingBankCallbackRequest,
            handle_issuing_bank_callback_request
        )(rq)

    return api
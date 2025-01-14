from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.iss_bank_new_pmt.logic import handle_issuing_bank_new_payment_request_from_payment_processor
from services.iss_bank_new_pmt.definition import issuing_bank_new_payment_service_definition


def api():

    definition: ServiceDefinition = issuing_bank_new_payment_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def new_payment(rq: IssuingBankNewCardPaymentRequest):
        return request_handler(
            definition,
            IssuingBankNewCardPaymentRequest,
            handle_issuing_bank_new_payment_request_from_payment_processor
        )(rq)

    return api
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewCardPaymentRequest
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.pmt_proc_new_pmt.logic import handle_new_card_payment_request_from_merchant_pos
from services.pmt_proc_new_pmt.definition import payment_processor_new_payment_service_definition

def api():

    definition: ServiceDefinition = payment_processor_new_payment_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def new_card_payment(rq: PaymentProcessorNewCardPaymentRequest):
        return request_handler(
            definition,
            PaymentProcessorNewCardPaymentRequest,
            handle_new_card_payment_request_from_merchant_pos
        )(rq)

    return api
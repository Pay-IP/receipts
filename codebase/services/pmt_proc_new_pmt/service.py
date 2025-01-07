from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.pmt_proc_new_pmt.logic import handle_payment_processor_new_customer_payment_request
from services.pmt_proc_new_pmt.definition import payment_processor_new_payment_service_definition

def api():

    definition: ServiceDefinition = payment_processor_new_payment_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def new_payment(rq: PaymentProcessorNewPaymentRequest):
        return request_handler(
            definition,
            PaymentProcessorNewPaymentRequest,
            handle_payment_processor_new_customer_payment_request
        )(rq)

    return api
from model.common import Service
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest
from util.service_base import register_healthcheck_endpoint
from util.structured_logging import configure_structured_logging
from fastapi import FastAPI
from util.service import request_handler
from services.pmt_proc_new_pmt.logic import handle_payment_processor_new_customer_payment_request

def api():

    api = FastAPI()
    configure_structured_logging(Service.PMT_PROC_NEW_PMT)

    register_healthcheck_endpoint(api)

    @api.post("/")
    def new_payment(rq: PaymentProcessorNewPaymentRequest):
        return request_handler(
            PaymentProcessorNewPaymentRequest,
            handle_payment_processor_new_customer_payment_request
        )(rq)

    return api
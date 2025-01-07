from model.common import Service
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest
from util.service import request_handler
from services.platform_new_pmt.logic import handle_platform_new_payment_request
from util.service_base import register_healthcheck_endpoint
from util.structured_logging import configure_structured_logging
from fastapi import FastAPI

def api():

    api = FastAPI()
    configure_structured_logging(Service.PLATFORM_NEW_PMT)

    register_healthcheck_endpoint(api)

    @api.post("/")
    def new_payment(rq: PlatformNewPaymentRequest):
        return request_handler(
            PlatformNewPaymentRequest, 
            handle_platform_new_payment_request
        )(rq)

    return api

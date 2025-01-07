from model.common import Service
from services.iss_bank_callback.rqrsp import IssuingBankCallbackRequest
from util.service_base import register_healthcheck_endpoint
from util.structured_logging import configure_structured_logging
from fastapi import FastAPI
from util.service import request_handler
from services.iss_bank_callback.logic import handle_issuing_bank_callback_request

def api():
    api = FastAPI()
    configure_structured_logging(Service.ISS_BANK_CALLBACK)

    register_healthcheck_endpoint(api)

    @api.post("/")
    def callback(rq: IssuingBankCallbackRequest):
        return request_handler(
            IssuingBankCallbackRequest,
            handle_issuing_bank_callback_request
        )(rq)

    return api
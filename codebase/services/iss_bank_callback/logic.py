from services.iss_bank_callback.rqrsp import IssuingBankCallbackRequest, IssuingBankCallbackResponse
from util.service_config_base import ServiceConfig

def handle_issuing_bank_callback_request(
    config: ServiceConfig,
    rq: IssuingBankCallbackRequest
):
    
    return IssuingBankCallbackResponse(
        rq=rq
    )
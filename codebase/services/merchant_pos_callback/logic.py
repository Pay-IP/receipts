from services.merchant_pos_callback.rqrsp import MerchantPosCallbackRequest, MerchantPosCallbackResponse
from util.service.service_config_base import ServiceConfig

def handle_merchant_pos_callback_request(
    config: ServiceConfig,
    rq: MerchantPosCallbackRequest
):
    return MerchantPosCallbackResponse()
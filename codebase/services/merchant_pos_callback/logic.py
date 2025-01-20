from services.merchant_pos_callback.rqrsp import PlatformReceiptMatchExternalNotification, MerchantPosCallbackResponse
from util.service.service_config_base import ServiceConfig

def handle_merchant_pos_callback_request(
    config: ServiceConfig,
    rq: PlatformReceiptMatchExternalNotification
):
    return MerchantPosCallbackResponse(
        ack=True
    )
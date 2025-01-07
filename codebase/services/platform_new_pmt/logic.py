from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest, PlatformNewPaymentResponse
from util.service_config_base import ServiceConfig

def handle_platform_new_payment_request(
    config: ServiceConfig,
    rq: PlatformNewPaymentRequest
):

    return PlatformNewPaymentResponse(
        rq=rq
    )
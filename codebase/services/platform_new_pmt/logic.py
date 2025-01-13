from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest, PlatformNewPaymentResponse
from util.service.service_config_base import ServiceConfig

def handle_platform_new_payment_request_from_customer_bank(
    config: ServiceConfig,
    rq: PlatformNewPaymentRequest
):

    return PlatformNewPaymentResponse(
        successful=True
    )
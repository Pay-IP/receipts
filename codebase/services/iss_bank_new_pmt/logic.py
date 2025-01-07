from services.iss_bank_new_pmt.rqrsp import IssuingBankNewPaymentRequest, IssuingBankNewPaymentResponse
from services.platform_new_pmt.client import PlatformNewPaymentClient
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest
from util.service.service_config_base import ServiceConfig

def handle_issuing_bank_new_payment_request(
    config: ServiceConfig,
    rq: IssuingBankNewPaymentRequest
):

    
    platform_new_pmt_rsp = PlatformNewPaymentClient().post(
        PlatformNewPaymentRequest(
            currency=rq.currency,
            currency_amount=rq.currency_amount
        )
    )

    return IssuingBankNewPaymentResponse(
        rq=rq
    )
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.platform_new_receipt.rqrsp import PlatformNewReceiptRequest
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest
from util.service_config_base import ServiceConfig

def handle_merchant_pos_new_checkout_request(
    config: ServiceConfig, 
    rq: MerchantPosNewCheckoutRequest
):
    
    payment = PaymentProcessorNewPaymentClient().post(
        PaymentProcessorNewPaymentRequest(
            currency=rq.currency,
            currency_amt=rq.total_amount_after_tax
    ))

    platform_receipt = PlatformNewReceiptClient().post(
        PlatformNewReceiptRequest(
        )
    )

    return MerchantPosNewCheckoutResponse(
        rq=rq
    )

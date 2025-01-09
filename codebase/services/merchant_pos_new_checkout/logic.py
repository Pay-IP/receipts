from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.platform_new_receipt.rqrsp import PlatformNewReceiptRequest
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.service.service_config_base import ServiceConfig


# merchant seed data required
# - currency
# - payment processor
# - SKUs

def handle_merchant_pos_new_checkout_request(
    config: ServiceConfig, 
    rq: MerchantPosNewCheckoutRequest
):
    
    # create invoice from request
    # - with line items

    # attempt to mke payment

    pmt_proc_rsp: PaymentProcessorNewPaymentResponse = PaymentProcessorNewPaymentClient().post(
        PaymentProcessorNewPaymentRequest(
            currency=rq.currency,
            currency_amt=rq.total_amount_after_tax
    ))

    # update invoice with payment details

    # create receipt for submission to platform

    platform_receipt = PlatformNewReceiptClient().post(
        PlatformNewReceiptRequest(
        )
    )

    return MerchantPosNewCheckoutResponse(
        rq=rq
    )

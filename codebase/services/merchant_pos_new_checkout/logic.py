from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.platform_new_receipt.rqrsp import PlatformNewReceiptRequest
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest
from util.env import endpoint_from_env

def handle_merchant_pos_new_checkout_request(client_id: int, rq: MerchantPosNewCheckoutRequest):

    pmt_proc_new_pmt_service = PaymentProcessorNewPaymentClient()
    
    payment = pmt_proc_new_pmt_service.post(
        PaymentProcessorNewPaymentRequest(
            currency=rq.currency,
            currency_amt=rq.total_amount_after_tax
    ))

    # platform new receipt
    platform_new_receipt_service = PlatformNewReceiptClient()
    platform_receipt = platform_new_receipt_service.post(
        PlatformNewReceiptRequest(
            
        )
    )

    return MerchantPosNewCheckoutResponse(
        rq=rq
    )

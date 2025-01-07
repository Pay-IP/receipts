from services.iss_bank_new_pmt.client import IssuingBankNewCustomerPaymentClient
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest, PlatformNewPaymentResponse

def handle_platform_new_payment_request(
    client_id: int, 
    rq: PlatformNewPaymentRequest
):
    
    iss_bank_new_pmt_service = IssuingBankNewCustomerPaymentClient()

    return PlatformNewPaymentResponse()
from services.iss_bank_new_pmt.rqrsp import IssuingBankPaymentExport, IssuingBankNewPaymentRequest, IssuingBankNewPaymentResponse
from services.platform_new_pmt.client import PlatformNewPaymentClient

def handle_issuing_bank_new_payment_request(
    client_id: int, 
    rq: IssuingBankNewPaymentRequest
):

    platform_new_pmt_service = PlatformNewPaymentClient()

    return IssuingBankNewPaymentResponse(
        payment=IssuingBankPaymentExport()
    )
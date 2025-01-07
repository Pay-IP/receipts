from services.iss_bank_new_pmt.client import IssuingBankNewCustomerPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse

def handle_payment_processor_new_customer_payment_request(
    client_id: int, 
    rq: PaymentProcessorNewPaymentRequest
):

    iss_bank_new_pmt_service = IssuingBankNewCustomerPaymentClient()

    return PaymentProcessorNewPaymentResponse(
        rq=rq
    )
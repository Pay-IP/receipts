from services.iss_bank_new_pmt.client import IssuingBankNewCustomerPaymentClient
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewPaymentRequest, IssuingBankNewPaymentResponse
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.service.service_config_base import ServiceConfig

def handle_payment_processor_new_customer_payment_request(
    config: ServiceConfig, 
    rq: PaymentProcessorNewPaymentRequest
):

    iss_bank_new_pmt_rsp: IssuingBankNewPaymentResponse = IssuingBankNewCustomerPaymentClient().post(
        IssuingBankNewPaymentRequest(
            currency=rq.currency,
            currency_amount=rq.currency_amt
        )
    )

    return PaymentProcessorNewPaymentResponse(
        rq=rq
    )
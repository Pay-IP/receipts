import datetime
import uuid
from model.write_model.objects.emv import IssuerEmvTransactionData
from services.iss_bank_new_pmt.client import IssuingBankNewCardPaymentClient
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewCardPaymentRequest, PaymentProcessorNewCardPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import serialize_datetime, serialize_uuid

def handle_new_card_payment_request_from_merchant_pos(
    config: ServiceConfig, 
    rq: PaymentProcessorNewCardPaymentRequest
):
    
    pmt_proc_unique_payment_reference = serialize_uuid(uuid.uuid4())
    pmt_proc_pmt_timestamp = datetime.datetime.now()





    iss_bank_new_pmt_rsp: IssuingBankNewCardPaymentResponse = IssuingBankNewCardPaymentClient().post(
        IssuingBankNewCardPaymentRequest(
            currency=rq.currency,
            currency_amount=rq.currency_amt,
            payment_processor_payment_reference=pmt_proc_unique_payment_reference
        )
    )



    return PaymentProcessorNewCardPaymentResponse(

        currency=rq.currency,
        currency_amt_paid=rq.currency_amt,
        original_merchant_reference=rq.reference,

        successful=iss_bank_new_pmt_rsp.successful,
        emv_data=emv_receipt,

        reference=pmt_proc_unique_payment_reference,
        timestamp=serialize_datetime(pmt_proc_pmt_timestamp)
    )
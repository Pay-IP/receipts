import datetime
import json
import uuid
from services.iss_bank_new_pmt.client import IssuingBankNewCustomerPaymentClient
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewPaymentRequest, IssuingBankNewPaymentResponse
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import serialize_datetime

import base64

def handle_payment_processor_new_customer_payment_request(
    config: ServiceConfig, 
    rq: PaymentProcessorNewPaymentRequest
):
    
    pmt_proc_unique_payment_reference = str(uuid.uuid4())
    pmt_proc_pmt_timestamp = datetime.datetime.now()

    iss_bank_new_pmt_rsp: IssuingBankNewPaymentResponse = IssuingBankNewCustomerPaymentClient().post(
        IssuingBankNewPaymentRequest(
            currency=rq.currency,
            currency_amount=rq.currency_amt,
            payment_processor_payment_reference=pmt_proc_unique_payment_reference
        )
    )

    meta_data = {
        "fish": "cat"
    }
    meta_data_json_str = json.dumps(meta_data)
    b4_encoded_meta_data = base64.b64encode(meta_data_json_str.encode('utf-8')).decode('utf-8')

    return PaymentProcessorNewPaymentResponse(

        currency=rq.currency,
        currency_amt_paid=rq.currency_amt,
        original_merchant_reference=rq.reference,

        successful=iss_bank_new_pmt_rsp.successful,
        meta_data_b64=b4_encoded_meta_data,

        reference=pmt_proc_unique_payment_reference,
        timestamp=serialize_datetime(pmt_proc_pmt_timestamp)
    )
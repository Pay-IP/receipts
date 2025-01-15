import uuid
from model.write_model.objects.emv import ISO8583_0200_FinReq, TerminalEmvReceipt
from services.iss_bank_new_pmt.client import IssuingBankNewCardPaymentClient
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewCardPaymentRequest, PaymentProcessorNewCardPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import serialize_uuid

def handle_new_card_payment_request_from_merchant_pos(
    config: ServiceConfig, 
    rq: PaymentProcessorNewCardPaymentRequest
):
    
    iso8583_rq = ISO8583_0200_FinReq(
        
        date = '',
        time = '',   
        currency_code = '',
        currency_amount = 0,

        merchant_address = '',

        pan = '',
        terminal_serial_number = '',
        terminal_system_trace_audit_number = '',

        emv_application_label = '',
        application_ID = '',

        CTQ = '',
        terminal_verification_results = '',
        application_cryptogram = '',

        unique_transaction_identifier = '',
        retrieval_reference_number = ''
    )

    payment_reference = uuid.uuid4()
    payment_reference_str = serialize_uuid(payment_reference)

    iss_bank_new_pmt_rsp: IssuingBankNewCardPaymentResponse = IssuingBankNewCardPaymentClient().post(
        IssuingBankNewCardPaymentRequest(
            iso8583_0200_fin_req=iso8583_rq,
            payment_processor_payment_reference=payment_reference_str
        )
    )

    return PaymentProcessorNewCardPaymentResponse(
        successful = iss_bank_new_pmt_rsp.authorized,
        payment_processor_payment_reference = serialize_uuid(payment_reference),
        terminal_emv_receipt = TerminalEmvReceipt(
            iso_0200_fin_req = iso8583_rq, 
            iso_0210_fin_rsp = iss_bank_new_pmt_rsp.iso8583_0210_fin_rsp
        )
    )
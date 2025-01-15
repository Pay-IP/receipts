import random
import uuid
from model.orm.query import insert_one, select_all, select_on_id
from model.write_model.objects.emv import ISO8583_0200_FinReqMsg, TerminalEmvReceipt
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccount
from model.write_model.objects.payment_processor_write_model import PaymentProcessorMerchant, PaymentProcessorMerchantTSN
from services.iss_bank_new_pmt.client import IssuingBankNewCardPaymentClient
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewCardPaymentRequest, PaymentProcessorNewCardPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import serialize_uuid

def handle_new_card_payment_request_from_merchant_pos(
    config: ServiceConfig, 
    rq: PaymentProcessorNewCardPaymentRequest,
    merchant_id = 1
):
    
    db_engine = config.write_model_db_engine()
    merchant = select_on_id(PaymentProcessorMerchant, merchant_id, db_engine)
    
    # this would normally happen out-of-band
    #
    issuing_bank_client_ac = random.sample(select_all(IssuingBankClientAccount, db_engine), 1)[0]
    card_pan = issuing_bank_client_ac.card_pan

    # generate acquirer EMV info from the above

    merchant_tsn =  PaymentProcessorMerchantTSN(merchant_id = merchant.id)
    merchant_tsn = insert_one(merchant_tsn, db_engine)
    merchant_tsn_str = str(merchant_tsn.tsn) # TODO generic correct serialization

    iso_0200_msg = ISO8583_0200_FinReqMsg(
        
        transaction_date = '',
        transaction_time = '',   
        
        currency_code = '',
        currency_amount = 0,

        merchant_address = merchant.address,

        pan = card_pan,
        terminal_serial_number = merchant_tsn_str, # TODO generic correct serialization
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
            iso_0200_fin_req=iso_0200_msg,
            payment_processor_payment_reference=payment_reference_str
        )
    )

    # create and persist payment record

    return PaymentProcessorNewCardPaymentResponse(
        successful = iss_bank_new_pmt_rsp.authorized,
        payment_processor_payment_reference = serialize_uuid(payment_reference),
        terminal_emv_receipt = TerminalEmvReceipt(
            iso_0200_fin_req = iso_0200_msg, 
            iso_0210_fin_rsp = iss_bank_new_pmt_rsp.iso_0210_fin_rsp
        )
    )
import datetime
import random
import uuid
from model.query import insert_one, select_all, select_on_id
from model.write_model.objects.emv import ISO8583_0200_FinReqMsg, ISO8583_02x0_MsgPair, TerminalEmvReceipt, formatted_terminal_serial_number, formatted_transaction_date, formatted_transaction_time, formatted_system_trace_audit_number, random_emv_CTQ, random_emv_application_cryptogram, formatted_retrieval_reference_number, random_terminal_verification_results, formatted_unique_transaction_identifier
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccount
from model.write_model.objects.payment_processor_write_model import PaymentProcessorMerchant, PaymentProcessorMerchantTSN, PaymentProcessorSystemTraceAuditNumber
from services.iss_bank_new_pmt.client import IssuingBankNewCardPaymentClient
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewCardPaymentRequest, PaymentProcessorNewCardPaymentResponse
from util.service.service_config_base import ServiceConfig

def handle_new_card_payment_request_from_merchant_pos(
    config: ServiceConfig, 
    rq: PaymentProcessorNewCardPaymentRequest,
    merchant_id = 1 # TODO source from auth
):
    
    db_engine = config.write_model_db_engine()
    merchant = select_on_id(PaymentProcessorMerchant, merchant_id, db_engine)
    
    # this would normally happen out-of-band
    #
    issuing_bank_client_ac = random.sample(select_all(IssuingBankClientAccount, db_engine), 1)[0]

    merchant_tsn =  PaymentProcessorMerchantTSN(merchant_id = merchant.id)
    merchant_tsn = insert_one(merchant_tsn, db_engine)
    tsn = formatted_terminal_serial_number(merchant_tsn.tsn)

    stan =  PaymentProcessorSystemTraceAuditNumber()
    stan = insert_one(stan, db_engine)

    guid = uuid.uuid4()

    transaction_timestamp = datetime.datetime.now()

    card_acc_idc = '000000002915551'

    iso_0200_msg = ISO8583_0200_FinReqMsg(
        
        transaction_date_str = formatted_transaction_date(transaction_timestamp),
        transaction_time_str = formatted_transaction_time(transaction_timestamp),
        
        currency_code = rq.currency,
        currency_amount = rq.currency_amt,

        merchant_address = merchant.address,

        pan = issuing_bank_client_ac.card_pan,
        terminal_serial_number = tsn,
        terminal_system_trace_audit_number = formatted_system_trace_audit_number(stan.stan),

        emv_application_label = issuing_bank_client_ac.card_app_label,
        application_ID = issuing_bank_client_ac.card_aid,

        CTQ = random_emv_CTQ(),
        terminal_verification_results = random_terminal_verification_results(),
        application_cryptogram = random_emv_application_cryptogram(),

        unique_transaction_identifier = formatted_unique_transaction_identifier(
            guid,
            card_acc_idc,
            tsn
        ),

        retrieval_reference_number = formatted_retrieval_reference_number(transaction_timestamp)
    )

    payment_id = uuid.uuid4()

    iss_bank_new_pmt_rsp: IssuingBankNewCardPaymentResponse = IssuingBankNewCardPaymentClient().post(
        IssuingBankNewCardPaymentRequest(
            iso_0200_fin_req=iso_0200_msg,
            payment_processor_payment_id=payment_id
        )
    )

    # create and persist payment record

    return PaymentProcessorNewCardPaymentResponse(
        successful = iss_bank_new_pmt_rsp.iso_0200_fin_rsp.authorized,
        payment_processor_payment_reference = payment_id,
        terminal_emv_receipt = TerminalEmvReceipt(
            iso=ISO8583_02x0_MsgPair(
                rq = iso_0200_msg, 
                rsp = iss_bank_new_pmt_rsp.iso_0200_fin_rsp
            )
        )
    )
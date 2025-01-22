import datetime
import uuid
from model.query import insert_one, select_all, select_first_on_filters, update_items
from model.write_model.objects.emv import ISO8583_0200_FinReqMsg, ISO8583_0210_FinRspMsg, ISO8583_02x0_MsgPair, random_auth_rsp_id
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccount, IssuingBankClientAccountDebit
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from services.platform_new_pmt.client import PlatformNewPaymentClient
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest, PlatformNewPaymentResponse
from services.trigger.rqrsp import NullRequest
from util.service.service_config_base import ServiceConfig

def authorize_customer_account_payment_request(db_engine, emv_req: ISO8583_0200_FinReqMsg) -> tuple[IssuingBankClientAccount, IssuingBankClientAccountDebit, ISO8583_0210_FinRspMsg]:
    
    client_ac = select_first_on_filters(
        IssuingBankClientAccount,
        { 'card_pan': emv_req.pan },
        db_engine
    )

    issuer_timestamp = datetime.datetime.now(),

    emv_rsp = ISO8583_0210_FinRspMsg(
        authorized = True,  
        authorization_response_identifier = random_auth_rsp_id()
    )

    ac_debit = insert_one(IssuingBankClientAccountDebit(
            client_account_id = client_ac.id,
            currency_amount = emv_req.currency_amount,
            timestamp = issuer_timestamp,
            platform_receipt_id = None,
            emv_rq = emv_req.dict(),
            emv_rsp = emv_rsp.dict(),
            external_id = uuid.uuid4()
        ),
        db_engine
    )
    
    return client_ac, ac_debit, emv_rsp

def handle_issuing_bank_new_payment_request_from_payment_processor(
    config: ServiceConfig,
    rq: IssuingBankNewCardPaymentRequest
):

    client_ac, ac_debit, iso_0210_fin_rsp = authorize_customer_account_payment_request(config.write_model_db_engine(), rq.iso_0200_fin_req)   

    iso_msgs = ISO8583_02x0_MsgPair(
        rq=rq.iso_0200_fin_req,
        rsp=iso_0210_fin_rsp
    )

    platform_rsp: PlatformNewPaymentResponse = PlatformNewPaymentClient().post(
        PlatformNewPaymentRequest(
            iso_msgs=iso_msgs,
            issuer_bank_customer_ac_external_id=client_ac.external_id,
            issuer_bank_payment_id=ac_debit.external_id
        )
    )

    ac_debit.platform_payment_id = platform_rsp.platform_payment_id
    update_items([ac_debit], config.write_model_db_engine())

    return IssuingBankNewCardPaymentResponse(
        iso_0200_fin_rsp = iso_0210_fin_rsp
    )

def handle_get_issuing_bank_client_accounts(
    config: ServiceConfig,
    _: NullRequest
) -> list[IssuingBankClientAccount]:

    return select_all(IssuingBankClientAccount, config.write_model_db_engine())

def handle_get_issuing_bank_client_account_debits(
    config: ServiceConfig,
    _: NullRequest
) -> list[IssuingBankClientAccountDebit]:
    
        return select_all(IssuingBankClientAccountDebit, config.write_model_db_engine())

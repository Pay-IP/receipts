import datetime
from uuid import UUID, uuid4

from model.orm.query import insert_one, select_first_on_filters
from model.write_model.objects.emv import ISO8583_0200_FinReqMsg, ISO8583_0210_FinRspMsg
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccount, IssuingBankClientAccountDebit
from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from services.platform_new_pmt.client import PlatformNewPaymentClient
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest
from util.service.service_config_base import ServiceConfig
from util.web import serialize_uuid


def customer_id_from_pan(pan: str) -> UUID:
    return uuid4()

def anonymous_external_facing_customer_id_for_internal_customer_id(internal_customer_id: UUID) -> UUID:
    return uuid4()

def new_authorization_response_identifier() -> str:
    return ''

def authorize_customer_account_payment_request(db_engine, emv_req: ISO8583_0200_FinReqMsg) -> tuple[IssuingBankClientAccount, ISO8583_0210_FinRspMsg]:
    
    client_ac = select_first_on_filters(
        IssuingBankClientAccount,
        { 'card_pan': emv_req.pan },
        db_engine
    )

    issuer_timestamp = datetime.datetime.now(),

    emv_rsp = ISO8583_0210_FinRspMsg(
        authorized = True,  
        authorization_response_identifier = new_authorization_response_identifier()
    )

    ac_debit = insert_one(IssuingBankClientAccountDebit(
            client_account_id = client_ac.id,
            currency_amount = emv_req.currency_amount,
            timestamp = issuer_timestamp,
            platform_receipt_id = None,
            emv_rq = emv_req.dict(),
            emv_rsp = emv_rsp.dict(),
        ),
        db_engine
    )
    
    return client_ac, emv_rsp

def handle_issuing_bank_new_payment_request_from_payment_processor(
    config: ServiceConfig,
    rq: IssuingBankNewCardPaymentRequest
):

    client_ac, iso_0210_fin_rsp = authorize_customer_account_payment_request(config.write_model_db_engine(), rq.iso_0200_fin_req)   
    #internal_customer_id = customer_id_from_pan(rq.iso_0200_fin_req.pan)
    anonymized_external_facing_customer_id = anonymous_external_facing_customer_id_for_internal_customer_id(client_ac.id)

    platform_new_pmt_rsp = PlatformNewPaymentClient().post(
        PlatformNewPaymentRequest(

            currency=rq.iso_0200_fin_req.currency_code,
            currency_amount=rq.iso_0200_fin_req.currency_amount,
            persistent_anonymized_customer_id=serialize_uuid(anonymized_external_facing_customer_id),
        )
    )

    return IssuingBankNewCardPaymentResponse(
        iso_0210_fin_rsp = iso_0210_fin_rsp,
        authorized=iso_0210_fin_rsp.authorized
    )
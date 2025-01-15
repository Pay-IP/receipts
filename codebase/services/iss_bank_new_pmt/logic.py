from uuid import UUID, uuid4

from model.write_model.objects.emv import ISO8583_0200_FinReqMsg, ISO8583_0210_FinRspMsg
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

def authorize_customer_payment(customer_id: UUID, fin_req: ISO8583_0200_FinReqMsg) -> ISO8583_0210_FinRspMsg:
    
    # TODO validate params and check available funds

    return ISO8583_0210_FinRspMsg(
        approved = True,  
        authorization_response_identifier = new_authorization_response_identifier()
    )


def handle_issuing_bank_new_payment_request_from_payment_processor(
    config: ServiceConfig,
    rq: IssuingBankNewCardPaymentRequest
):

    # verify customer    
    internal_customer_id = customer_id_from_pan(rq.iso_0200_fin_req.pan)
    emv_authorization_rsp = authorize_customer_payment(internal_customer_id, rq.iso_0200_fin_req)

    anonymized_external_facing_customer_id = anonymous_external_facing_customer_id_for_internal_customer_id(internal_customer_id)

    platform_new_pmt_rsp = PlatformNewPaymentClient().post(
        PlatformNewPaymentRequest(
            
            currency=rq.iso_0200_fin_req.currency_code,
            currency_amount=rq.iso_0200_fin_req.currency_amount,
            
            persistent_anonymized_customer_id=serialize_uuid(anonymized_external_facing_customer_id),
        )
    )

    return IssuingBankNewCardPaymentResponse(
        iso_0210_fin_rsp = emv_authorization_rsp,
        authorized=emv_authorization_rsp.approved
    )
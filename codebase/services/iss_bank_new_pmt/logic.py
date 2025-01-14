from uuid import UUID, uuid4

from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from services.platform_new_pmt.client import PlatformNewPaymentClient
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest
from util.service.service_config_base import ServiceConfig
from util.web import serialize_uuid


def customer_id_from_rq(rq: IssuingBankNewCardPaymentRequest) -> UUID:
    return uuid4()

def anonymous_external_facing_customer_id_for_internal_customer_id(internal_customer_id: UUID) -> UUID:
    return uuid4()

def handle_issuing_bank_new_payment_request_from_payment_processor(
    config: ServiceConfig,
    rq: IssuingBankNewCardPaymentRequest
):
    
    internal_customer_id = customer_id_from_rq(rq)
    anonymized_external_facing_customer_id = anonymous_external_facing_customer_id_for_internal_customer_id(internal_customer_id)

    platform_new_pmt_rsp = PlatformNewPaymentClient().post(
        PlatformNewPaymentRequest(
            
            currency=rq.currency,
            currency_amount=rq.currency_amount,
            
            persistent_anonymized_customer_id=serialize_uuid(anonymized_external_facing_customer_id),
        )
    )

    issuer_emv_data = EmvIssuerData(
        
    )

    return IssuingBankNewCardPaymentResponse(
        
        successful = True,
        
        currency = rq.currency,
        currency_amount_paid = rq.currency_amount
    )
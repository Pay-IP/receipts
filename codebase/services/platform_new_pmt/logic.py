import datetime
import uuid
from model.query import insert_one, select_all, select_all_on_filters
from model.write_model.objects.platform_write_model import PlatformBank, PlatformBankClientAccount, PlatformBankClientAccountPayment
from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest, PlatformNewPaymentResponse
from util.service.service_config_base import ServiceConfig

def handle_new_payment_request_to_platform_from_customer_bank(
    config: ServiceConfig,
    rq: PlatformNewPaymentRequest
):
    engine = config.write_model_db_engine()

    # TODO = get from auth
    bank = select_all(PlatformBank, engine)[0]
    
    # lookup PlatformBankClientAccount, create if it DNE

    bank_client_acs = select_all_on_filters(
        PlatformBankClientAccount,
        { 
            'issuer_bank_client_ac_id': rq.issuer_bank_customer_ac_external_id,
            'bank_id': bank.id
        },
        engine
    )

    bank_client_ac = None
    if len(bank_client_acs) > 0:
        bank_client_ac = bank_client_acs[0]
        # TODO handle multiples
    else:
        bank_client_ac = PlatformBankClientAccount(
            bank_id = bank.id,
            issuer_bank_client_ac_id = rq.issuer_bank_customer_ac_external_id,
            external_id = uuid.uuid4()
        )
        bank_client_ac = insert_one(bank_client_ac, engine)

    payment = PlatformBankClientAccountPayment(
        external_id = uuid.uuid4(),                         
        bank_client_ac = bank_client_ac,
        bank_payment_id = rq.issuer_bank_payment_id,
        system_timestamp=datetime.datetime.now(),
        payment=rq.iso_msgs.model_dump_json()
    )

    payment = insert_one(payment, config.write_model_db_engine())

    return PlatformNewPaymentResponse(
        platform_payment_id=payment.external_id
    )
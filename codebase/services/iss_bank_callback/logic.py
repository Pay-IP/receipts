from model.query import select_first_on_filters, update_items
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccountDebit
from services.iss_bank_callback.rqrsp import PlatformPaymentMatchExternalNotification, IssuingBankCallbackResponse
from util.service.service_config_base import ServiceConfig

def handle_callback_notification_from_platform(
    config: ServiceConfig,
    rq: PlatformPaymentMatchExternalNotification
):
    
    db_engine = config.write_model_db_engine()
    
    client_ac_debit: IssuingBankClientAccountDebit = select_first_on_filters(
        IssuingBankClientAccountDebit,
        {
            'platform_payment_id': rq.platform_payment_id    
        },
        db_engine
    )

    client_ac_debit.platform_receipt_id = rq.platform_receipt_id,
    client_ac_debit.platform_receipt = rq.platform_receipt.model_dump_json()

    update_items([client_ac_debit], db_engine)

    return IssuingBankCallbackResponse(
        ack=True
    )
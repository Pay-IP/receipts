from services.iss_bank_callback.rqrsp import PlatformPaymentMatchNotification, IssuingBankCallbackResponse
from util.service.service_config_base import ServiceConfig

def handle_callback_notification_from_platform(
    config: ServiceConfig,
    rq: PlatformPaymentMatchNotification
):
    
    # TODO
    # update payment with platform_receipt_id
    # fetch platform_receipt_info from platform_new_receipt_service
    # save platform receipt info against original payment
    
    
    return IssuingBankCallbackResponse(
        rq=rq
    )
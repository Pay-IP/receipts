from services.iss_bank_callback.rqrsp import PlatformPaymentMatchExternalNotification
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.iss_bank_callback.logic import handle_callback_notification_from_platform
from services.iss_bank_callback.definition import issuing_bank_callback_service_definition

def api():

    definition: ServiceDefinition = issuing_bank_callback_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def callback(rq: PlatformPaymentMatchExternalNotification):
        return request_handler(
            definition,
            PlatformPaymentMatchExternalNotification,
            handle_callback_notification_from_platform
        )(rq)

    return api
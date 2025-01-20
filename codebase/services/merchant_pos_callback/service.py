from services.merchant_pos_callback.rqrsp import PlatformReceiptMatchExternalNotification
from util.service.service_base import ServiceDefinition, api_for_service_definition
from util.service.service_base import request_handler
from services.merchant_pos_callback.logic import handle_merchant_pos_callback_request
from services.merchant_pos_callback.definition import merchant_pos_callback_service_definition

def api():

    definition: ServiceDefinition = merchant_pos_callback_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def callback(rq: PlatformReceiptMatchExternalNotification):
        return request_handler(
            definition,
            PlatformReceiptMatchExternalNotification,
            handle_merchant_pos_callback_request
        )(rq)

    return api
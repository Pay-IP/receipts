from model.write_model.objects.platform_common import PlatformMerchantReceiptDTO
from util.service.service_base import ServiceDefinition, api_for_service_definition, request_handler
from services.platform_new_receipt.logic import handle_new_receipt_from_merchant_pos
from services.platform_new_receipt.definition import platform_new_receipt_service_definition

def api():

    definition: ServiceDefinition = platform_new_receipt_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def new_platform_receipt(rq: PlatformMerchantReceiptDTO):
        return request_handler(
            definition,
            PlatformMerchantReceiptDTO, 
            handle_new_receipt_from_merchant_pos
        )(rq)
    
    return api
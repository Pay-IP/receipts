from util.service.service_base import ServiceDefinition, api_for_service_definition
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest
from util.service.service_base import request_handler
from services.merchant_pos_new_checkout.logic import handle_get_merchant_sku_by_id, handle_get_merchant_skus, handle_merchant_pos_new_checkout_request
from services.merchant_pos_new_checkout.definition import merchant_pos_new_checkout_service_definition

def api():

    definition: ServiceDefinition = merchant_pos_new_checkout_service_definition()    
    api = api_for_service_definition(definition)

    @api.post("/")
    def checkout(rq: MerchantPosNewCheckoutRequest):
        return request_handler(
            definition,
            MerchantPosNewCheckoutRequest, 
            handle_merchant_pos_new_checkout_request
        )(rq)
    
    # these methods are here for convenience for internal testing
    # NOT FOR PRODUCTION USE - move to dedicated microservice

    @api.get("/skus")
    def get_merchant_skus():
        return request_handler(
            definition,
            None, 
            handle_get_merchant_skus
        )()

    @api.get("/sku/{id}")
    def get_merchant_sku_by_id(id):
        return request_handler(
            definition,
            None,
            handle_get_merchant_sku_by_id
        )(id)


    return api
from model.object_model.core.endpoint import Endpoint
from model.object_model.core.service import Service
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase

class MerchantPosNewCheckoutClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.MERCHANT_POS_NEW_CHECKOUT)):
        super().__init__(endpoint, MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse)
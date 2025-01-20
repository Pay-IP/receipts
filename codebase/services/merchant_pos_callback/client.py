from model.core.objects.service import Service

from model.core.objects.endpoint import Endpoint
from services.merchant_pos_callback.rqrsp import MerchantPosCallbackResponse, PlatformReceiptMatchNotification
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase

class MerchantPosCallbackClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.MERCHANT_POS_CALLBACK)):
        super().__init__(endpoint, PlatformReceiptMatchNotification, MerchantPosCallbackResponse)

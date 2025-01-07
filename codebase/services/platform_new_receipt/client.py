from services.platform_new_receipt.rqrsp import PlatformNewReceiptRequest, PlatformNewReceiptResponse
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase
from model.common import Endpoint, Service

class PlatformNewReceiptClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.PLATFORM_NEW_RECEIPT)):
        super().__init__(endpoint, PlatformNewReceiptRequest, PlatformNewReceiptResponse)

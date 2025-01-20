from model.write_model.objects.platform_common import PlatformMerchantReceiptDTO
from services.platform_new_receipt.rqrsp import PlatformReceiptResponse
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase
from model.core.objects.endpoint import Endpoint
from model.core.objects.service import Service

class PlatformNewReceiptClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.PLATFORM_NEW_RECEIPT)):
        super().__init__(endpoint, PlatformMerchantReceiptDTO, PlatformReceiptResponse)

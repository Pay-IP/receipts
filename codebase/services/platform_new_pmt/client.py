from services.platform_new_pmt.rqrsp import PlatformNewPaymentRequest, PlatformNewPaymentResponse
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase
from model.core.objects.endpoint import Endpoint
from model.core.objects.service import Service

class PlatformNewPaymentClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.PLATFORM_NEW_PMT)):
        super().__init__(endpoint, PlatformNewPaymentRequest, PlatformNewPaymentResponse)

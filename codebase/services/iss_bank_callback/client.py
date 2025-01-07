from services.iss_bank_callback.rqrsp import IssuingBankCallbackRequest, IssuingBankCallbackResponse
from model.common import Endpoint, Service
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase

class IssuingBankCallbackClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.ISS_BANK_CALLBACK)):
        super().__init__(endpoint, IssuingBankCallbackRequest, IssuingBankCallbackResponse)

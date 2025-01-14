from services.iss_bank_new_pmt.rqrsp import IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse
from model.core.objects.endpoint import Endpoint
from model.core.objects.service import Service
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase

class IssuingBankNewCardPaymentClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.ISS_BANK_NEW_PMT)):
        super().__init__(endpoint, IssuingBankNewCardPaymentRequest, IssuingBankNewCardPaymentResponse)

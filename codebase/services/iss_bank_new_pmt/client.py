from services.iss_bank_new_pmt.rqrsp import IssuingBankNewPaymentRequest, IssuingBankNewPaymentResponse
from model.object_model.core.endpoint import Endpoint
from model.object_model.core.service import Service
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase

class IssuingBankNewCustomerPaymentClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.ISS_BANK_NEW_PMT)):
        super().__init__(endpoint, IssuingBankNewPaymentRequest, IssuingBankNewPaymentResponse)

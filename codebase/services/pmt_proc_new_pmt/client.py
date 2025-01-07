
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase
from model.common import Endpoint, Service


class PaymentProcessorNewPaymentClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.PMT_PROC_NEW_PMT)):
        super().__init__(endpoint, PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse)
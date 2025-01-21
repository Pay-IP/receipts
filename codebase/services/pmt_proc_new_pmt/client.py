import datetime
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewCardPaymentRequest, PaymentProcessorNewCardPaymentResponse
from util.env import service_endpoint_from_env
from util.service.service_client_base import ServiceClientBase
from model.core.objects.endpoint import Endpoint
from model.core.objects.service import Service
from util.web import serialize_datetime

class PaymentProcessorNewPaymentClient(ServiceClientBase):

    def __init__(self, endpoint: Endpoint = service_endpoint_from_env(Service.PMT_PROC_NEW_PMT)):
        super().__init__(endpoint, PaymentProcessorNewCardPaymentRequest, PaymentProcessorNewCardPaymentResponse)

    def new_card_payment(self, 
        currency: str, 
        currency_amt: int, 
        timestamp: datetime.datetime, 
        reference: str
    ) -> PaymentProcessorNewCardPaymentResponse:
        return self.post(
            PaymentProcessorNewCardPaymentRequest(
                currency=currency,
                currency_amt=currency_amt,
                invoice_timestamp=serialize_datetime(timestamp),
                merchant_reference=reference
        ))

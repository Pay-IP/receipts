from pydantic import BaseModel

from model.object_model.write_model.common import Currency


class PaymentProcessorNewPaymentRequest(BaseModel):
    currency: str
    currency_amt: int

class PaymentProcessorNewPaymentResponse(BaseModel):
    rq: PaymentProcessorNewPaymentRequest
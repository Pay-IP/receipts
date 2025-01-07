from pydantic import BaseModel

from model.common import Currency

class PaymentProcessorNewPaymentRequest(BaseModel):
    currency: Currency
    currency_amt: int

class PaymentProcessorNewPaymentResponse(BaseModel):
    rq: PaymentProcessorNewPaymentRequest
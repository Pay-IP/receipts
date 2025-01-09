from pydantic import BaseModel

from model.object_model.write_model.payment_processor_write_model import Currency

class PaymentProcessorNewPaymentRequest(BaseModel):
    currency: Currency
    currency_amt: int

class PaymentProcessorNewPaymentResponse(BaseModel):
    rq: PaymentProcessorNewPaymentRequest
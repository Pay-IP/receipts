from pydantic import BaseModel

class PaymentProcessorNewPaymentRequest(BaseModel):
    currency: str
    currency_amt: int

class PaymentProcessorNewPaymentResponse(BaseModel):
    currency: str
    currency_amt: int
    reference: str
    successful: bool
    timestamp: str
from pydantic import BaseModel

class PlatformNewPaymentRequest(BaseModel):
    currency: str
    currency_amount: int

class PlatformNewPaymentResponse(BaseModel):
    rq: PlatformNewPaymentRequest
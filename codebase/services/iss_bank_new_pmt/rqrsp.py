from pydantic import BaseModel

class IssuingBankNewPaymentRequest(BaseModel):
    currency: str
    currency_amount: int

class IssuingBankNewPaymentResponse(BaseModel):
    rq: IssuingBankNewPaymentRequest
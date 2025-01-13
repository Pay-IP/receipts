from pydantic import BaseModel

class IssuingBankNewPaymentRequest(BaseModel):
    currency: str
    currency_amount: int
    payment_processor_payment_reference: str

class IssuingBankNewPaymentResponse(BaseModel):
    successful: bool
    currency: str
    currency_amount_paid: int
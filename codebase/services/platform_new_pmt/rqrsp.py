from pydantic import BaseModel

class PlatformNewPaymentRequest(BaseModel):
    
    currency: str
    currency_amount: int

    persistent_anonymized_customer_id: str

class PlatformNewPaymentResponse(BaseModel):
    successful: bool
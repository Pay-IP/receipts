from uuid import UUID
from pydantic import BaseModel

class PlatformPaymentMatchNotification(BaseModel):
    platform_payment_id: UUID
    platform_receipt_id: UUID

class IssuingBankCallbackResponse(BaseModel):
    pass
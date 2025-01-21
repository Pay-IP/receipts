from uuid import UUID
from pydantic import BaseModel

from model.write_model.objects.platform_common import PlatformReceiptForIssuingBank

class PlatformPaymentMatchExternalNotification(BaseModel):
    platform_payment_id: UUID
    platform_receipt_id: UUID
    platform_receipt: PlatformReceiptForIssuingBank

class IssuingBankCallbackResponse(BaseModel):
    ack: bool
from uuid import UUID
from pydantic import BaseModel

class PlatformReceiptMatchExternalNotification(BaseModel):
    platform_receipt_id: UUID
    platform_client_ac_id: UUID

class MerchantPosCallbackResponse(BaseModel):
    ack: bool
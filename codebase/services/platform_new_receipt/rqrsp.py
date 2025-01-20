from uuid import UUID
from pydantic import BaseModel

class PlatformReceiptResponse(BaseModel):
    platform_receipt_id: UUID
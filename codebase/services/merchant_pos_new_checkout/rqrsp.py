from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class MerchantPosNewCheckoutRequestItem(BaseModel):
    sku_id: int
    sku_count: int

class MerchantPosNewCheckoutRequest(BaseModel):
    items: list[MerchantPosNewCheckoutRequestItem]
    currency: str
    card_pan_for_demo: Optional[str]

class MerchantPosNewCheckoutResponse(BaseModel):
    successful: bool
    platform_receipt_id: UUID

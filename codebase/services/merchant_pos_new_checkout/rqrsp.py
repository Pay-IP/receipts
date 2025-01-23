from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class MerchantPosNewCheckoutRequestItem(BaseModel):

    sku_id: int
    sku_count: int
    sku_name: str
    sku_unit_price: int

class MerchantPosNewCheckoutRequest(BaseModel):

    items: list[MerchantPosNewCheckoutRequestItem]
    currency: str

class MerchantPosNewCheckoutResponse(BaseModel):
    successful: bool
    platform_receipt_id: UUID

from enum import Enum
from pydantic import BaseModel

class PlatformPaymentChannelEnum(Enum):
    CASH = "CASH"
    CARD = "CARD"
    CHECK = "CHECK"
    BANK_TRANSFER = "BANK_TRANSFER"

class PlatformReceiptLine(BaseModel):
    description: str
    count: int
    total_amount: int

class PlatformPaymentChannelPaymentData(BaseModel):
    payment_channel: str
    payment_channel_payment_reference: str

class PlatformReceiptTotals(BaseModel):
    total_amount_before_tax: int
    sales_tax_amount: int
    total_amount_after_tax: int

class PlatformReceiptRequest(BaseModel):
    
    merchant_reference: str

    invoice_datetime: str
    invoice_currency: str
    
    invoice_lines: list[PlatformReceiptLine]
    invoice_totals: PlatformReceiptTotals

    payment_channel_payment_data: PlatformPaymentChannelPaymentData


class PlatformReceiptResponse(BaseModel):
    receipt_id: str
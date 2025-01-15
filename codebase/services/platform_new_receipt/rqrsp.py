from enum import Enum
from pydantic import BaseModel

from model.write_model.objects.emv import TerminalEmvReceipt

class ReceiptLine(BaseModel):
    description: str
    count: int
    total_amount: int

class ReceiptTotals(BaseModel):
    total_amount_before_tax: int
    sales_tax_amount: int
    total_amount_after_tax: int

class PlatformReceiptRequest(BaseModel):
    
    merchant_reference: str

    invoice_datetime: str
    invoice_currency: str
    
    invoice_lines: list[ReceiptLine]
    invoice_totals: ReceiptTotals

    terminal_emv_receipt: TerminalEmvReceipt


class PlatformReceiptResponse(BaseModel):
    receipt_id: str
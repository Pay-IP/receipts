from enum import Enum
from pydantic import BaseModel
from uuid import UUID

class PlatformReceiptLine(BaseModel):
    description: str
    count: int
    total_amount: int

class PlatformReceiptTotals(BaseModel):
    total_amount_before_tax: int
    sales_tax_amount: int
    total_amount_after_tax: int


class PlatformEmvReceipt(BaseModel):

    merchant_address: str

    transaction_date_str: str
    transaction_time_str: str    

    authorized: bool  

    masked_pan: str
    terminal_serial_number: str
    retrieval_reference_number: str
    authorization_response_identifier: str
    emv_application_label: str

    unique_transaction_identifier: str

    currency_code: str
    currency_amount: int
    
    application_ID: str
    CTQ: str
    terminal_verification_results: str
    application_cryptogram: str

class PlatformMerchantReceiptDTO(BaseModel):
    
    merchant_receipt_id: UUID

    invoice_datetime: str
    invoice_currency: str
    
    invoice_lines: list[PlatformReceiptLine]
    invoice_totals: PlatformReceiptTotals

    emv_receipt: PlatformEmvReceipt

from enum import Enum
from pydantic import BaseModel

class ReceiptLine(BaseModel):
    description: str
    count: int
    total_amount: int

class ReceiptTotals(BaseModel):
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

class PlatformReceiptRequest(BaseModel):
    
    merchant_reference: str

    invoice_datetime: str
    invoice_currency: str
    
    invoice_lines: list[ReceiptLine]
    invoice_totals: ReceiptTotals

    emv_receipt: PlatformEmvReceipt


class PlatformReceiptResponse(BaseModel):
    receipt_id: str
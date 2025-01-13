from pydantic import BaseModel

class PaymentProcessorNewPaymentRequest(BaseModel):

    currency: str
    currency_amt: int

    reference: str
    invoice_timestamp: str

class PaymentProcessorNewPaymentResponse(BaseModel):

    currency: str
    currency_amt_paid: int
    original_merchant_reference: str

    successful: bool
    meta_data_b64: str # EMV data

    reference: str
    timestamp: str
    
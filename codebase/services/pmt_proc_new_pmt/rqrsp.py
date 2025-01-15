from pydantic import BaseModel

from model.write_model.objects.emv import TerminalEmvReceipt

class PaymentProcessorNewCardPaymentRequest(BaseModel):

    currency: str
    currency_amt: int
    merchant_reference: str


class PaymentProcessorNewCardPaymentResponse(BaseModel):

    successful: bool
    payment_processor_payment_reference: str
    terminal_emv_receipt: TerminalEmvReceipt 
    
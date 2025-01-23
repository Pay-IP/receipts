from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from model.write_model.objects.emv import TerminalEmvReceipt

class PaymentProcessorNewCardPaymentRequest(BaseModel):

    currency: str
    currency_amt: int
    merchant_payment_id: UUID
    card_PAN_for_demo: Optional[str]


class PaymentProcessorNewCardPaymentResponse(BaseModel):

    successful: bool
    payment_processor_payment_reference: UUID
    terminal_emv_receipt: TerminalEmvReceipt 
    
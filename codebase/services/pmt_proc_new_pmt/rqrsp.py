from pydantic import BaseModel

from model.write_model.objects.emv import AcquirerEmvTransactionData, IssuerEmvTransactionData

class PaymentProcessorNewCardPaymentRequest(BaseModel):

    currency: str
    currency_amt: int
    merchant_reference: str


class PaymentProcessorEmvData(BaseModel):

    acquirer_emv_data: AcquirerEmvTransactionData 
    issuer_emv_data: IssuerEmvTransactionData


class PaymentProcessorNewCardPaymentResponse(BaseModel):

    successful: bool
    original_merchant_reference: str
    emv_data: PaymentProcessorEmvData 
    
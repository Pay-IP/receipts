from pydantic import BaseModel

from model.write_model.objects.emv import AcquirerEmvTransactionData, IssuerEmvTransactionData

class IssuingBankNewCardPaymentRequest(BaseModel):
    acquirer_emv_data: AcquirerEmvTransactionData

class IssuingBankNewCardPaymentResponse(BaseModel):
    issuer_emv_data: IssuerEmvTransactionData
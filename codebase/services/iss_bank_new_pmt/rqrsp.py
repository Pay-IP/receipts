from pydantic import BaseModel

from model.write_model.objects.emv import ISO8583_0200_FinReqMsg, ISO8583_0210_FinRspMsg
class IssuingBankNewCardPaymentRequest(BaseModel):
    payment_processor_payment_reference: str
    iso_0200_fin_req: ISO8583_0200_FinReqMsg

class IssuingBankNewCardPaymentResponse(BaseModel):
    iso_0200_fin_rsp: ISO8583_0210_FinRspMsg
from pydantic import BaseModel

from model.write_model.objects.emv import ISO8583_0200_FinReq, ISO8583_0210_FinRsp

class IssuingBankNewCardPaymentRequest(BaseModel):

    payment_processor_payment_reference: str
    iso8583_0200_fin_req: ISO8583_0200_FinReq

class IssuingBankNewCardPaymentResponse(BaseModel):
    iso8583_0210_fin_rsp: ISO8583_0210_FinRsp
    authorized: bool
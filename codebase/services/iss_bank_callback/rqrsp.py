from pydantic import BaseModel

class IssuingBankCallbackRequest(BaseModel):
    pass

class IssuingBankCallbackResponse(BaseModel):
    rq: IssuingBankCallbackRequest
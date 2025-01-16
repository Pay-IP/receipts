from uuid import UUID
from pydantic import BaseModel

from model.write_model.objects.emv import ISO8583_02x0_MsgPair

class PlatformNewPaymentRequest(BaseModel):
    
    iso_msgs: ISO8583_02x0_MsgPair
    issuer_bank_customer_ac_external_id: UUID

class PlatformNewPaymentResponse(BaseModel):
    successful: bool
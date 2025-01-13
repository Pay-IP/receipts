import uuid
from services.platform_new_receipt.rqrsp import PlatformReceiptRequest, PlatformReceiptResponse
from util.web import serialize_uuid

def handle_platform_new_receipt_request(client_id: int, rq: PlatformReceiptRequest):
    
    # persist receipt
    
    return PlatformReceiptResponse(
        receipt_id=serialize_uuid(uuid.uuid4())
    )


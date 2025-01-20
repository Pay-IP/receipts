import datetime
import uuid
from model.query import insert_one, select_on_id
from model.write_model.objects.platform_common import PlatformMerchantReceiptDTO
from model.write_model.objects.platform_write_model import PlatformMerchant, PlatformMerchantReceipt
from services.platform_new_receipt.rqrsp import PlatformReceiptResponse
from util.service.service_config_base import ServiceConfig

def handle_new_receipt_from_merchant_pos(
    config: ServiceConfig, 
    merchant_receipt_data: PlatformMerchantReceiptDTO
):
    db_engine = config.write_model_db_engine()

    merchant_id = 1 # TODO source from auth
    merchant = select_on_id(PlatformMerchant, merchant_id, db_engine)

    merchant_receipt = PlatformMerchantReceipt(
        merchant = merchant,

        external_id = uuid.uuid4(),
        merchant_receipt_id = merchant_receipt_data.merchant_receipt_id,
        system_timestamp = datetime.datetime.now(),

        receipt = merchant_receipt_data.model_dump_json()
    )

    # PlatformMerchantReceiptDTO

    merchant_receipt = insert_one(merchant_receipt, db_engine)

    return PlatformReceiptResponse(
        platform_receipt_id=merchant_receipt.external_id
    )


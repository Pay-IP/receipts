import datetime
from model.query import select_all_on_filters, update_existing_items
from model.write_model.objects.emv import ISO8583_02x0_MsgPair, mask_pan
from model.write_model.objects.platform_common import PlatformEmvReceipt, PlatformMerchantReceiptDTO
from model.write_model.objects.platform_write_model import PlatformBankClientAccountPayment, PlatformMerchantReceipt
import schedule
import time

from util.service.service_config_base import ServiceConfig

JOB_PERIOD_S = 1
WAIT_PERIOD_S = 0.1


def get_unmatched_receipts(db_engine) -> list[PlatformMerchantReceipt]:

    unmatched_receipts = select_all_on_filters(
        PlatformMerchantReceipt,
        {   
            'is_matched': False
        },
        db_engine
    )

    return unmatched_receipts

def get_unmatched_payments(db_engine) -> list[PlatformBankClientAccountPayment]:
    
    unmatched_payments = select_all_on_filters(
        PlatformBankClientAccountPayment,
        {   
            'merchant_receipt_id': None
        },
        db_engine
    )

    return unmatched_payments

def match_job(config: ServiceConfig):

    print(f'match job running ... {datetime.datetime.now()}')
    db_engine = config.write_model_db_engine()
    
    # TODO for time window
    unmatched_payments = get_unmatched_payments(db_engine)
    unmatched_receipts = get_unmatched_receipts(db_engine)

    for payment in unmatched_payments:

        iso_msgs = ISO8583_02x0_MsgPair.parse_raw(payment.payment) # TODO rename to iso_msgs !!!

        hpan = mask_pan(iso_msgs.rq.pan)
        currency_amt = iso_msgs.rq.currency_amount
        auth_id_rsp = iso_msgs.rsp.authorization_response_identifier
        txn_date = iso_msgs.rq.transaction_date_str

        currency = iso_msgs.rq.currency_code
        merchant_address = iso_msgs.rq.merchant_address
        
        for receipt in unmatched_receipts:

            receiptDTO = PlatformMerchantReceiptDTO.parse_raw(receipt.receipt)
            emv: PlatformEmvReceipt = receiptDTO.emv_receipt

            if (
                emv.masked_pan == hpan,
                emv.currency_amount == currency_amt,
                emv.authorization_response_identifier == auth_id_rsp,
                emv.transaction_date_str == txn_date
            ):

                receipt.is_matched = True
                payment.merchant_receipt = receipt

                update_existing_items([receipt, payment], db_engine)

                # notify merchant via callback
                # notify bank via callback


def before_launching_platform_matching_rest_server(config: ServiceConfig):

    def launch_match_job():
        match_job(config)

    schedule.every(JOB_PERIOD_S).seconds.do(launch_match_job)

    while True:
        schedule.run_pending()
        time.sleep(WAIT_PERIOD_S)
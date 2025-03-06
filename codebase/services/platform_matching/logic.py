import datetime
from model.core.objects.endpoint import Endpoint, endpoint_from_url
from model.query import select_all_on_filters, update_items
from model.write_model.objects.emv import ISO8583_02x0_MsgPair, mask_pan
from model.write_model.objects.platform_common import PlatformEmvReceipt, PlatformMerchantReceiptDTO, PlatformReceiptForIssuingBank
from model.write_model.objects.platform_write_model import PlatformBankClientAccount, PlatformBankClientAccountPayment, PlatformMerchantReceipt
import schedule
import time

from services.iss_bank_callback.client import IssuingBankCallbackClient
from services.iss_bank_callback.rqrsp import PlatformPaymentMatchExternalNotification
from services.merchant_pos_callback.client import MerchantPosCallbackClient
from services.merchant_pos_callback.rqrsp import PlatformReceiptMatchExternalNotification
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

    db_engine = config.write_model_db_engine()

    # TODO for time window
    unmatched_payments: list[PlatformBankClientAccountPayment] = get_unmatched_payments(db_engine)
    unmatched_receipts: list[PlatformMerchantReceipt] = get_unmatched_receipts(db_engine)

    for payment in unmatched_payments:

        iso_msgs = ISO8583_02x0_MsgPair.model_validate(payment.payment)

        hpan = mask_pan(iso_msgs.rq.pan)
        currency_amt = iso_msgs.rq.currency_amount
        auth_id_rsp = iso_msgs.rsp.authorization_response_identifier
        txn_date = iso_msgs.rq.transaction_date_str

        currency = iso_msgs.rq.currency_code
        merchant_address = iso_msgs.rq.merchant_address
        
        for receipt in unmatched_receipts:

            receiptDTO = PlatformMerchantReceiptDTO.model_validate(receipt.receipt)
            merchant_emv_receipt: PlatformEmvReceipt = receiptDTO.emv_receipt

            if (
                merchant_emv_receipt.masked_pan == hpan and
                merchant_emv_receipt.currency_amount == currency_amt and
                merchant_emv_receipt.authorization_response_identifier == auth_id_rsp and
                merchant_emv_receipt.transaction_date_str == txn_date
            ):
                
                print(f'matched receipt {receipt.id} to payment {payment.id} on: {merchant_emv_receipt.authorization_response_identifier}')

                unmatched_receipts.remove(receipt)

                receipt.is_matched = True

                payment.merchant_receipt_id = receipt.id

                update_items([receipt, payment], db_engine)

                platform_bank_client_ac: PlatformBankClientAccount = payment.bank_client_ac 

                IssuingBankCallbackClient(
                    endpoint_from_url(platform_bank_client_ac.bank.callback_url)
                ).post(
                    PlatformPaymentMatchExternalNotification(
                        platform_payment_id=payment.external_id,
                        platform_receipt_id=receipt.external_id,
                        platform_receipt=PlatformReceiptForIssuingBank(

                            platform_merchant_id = receipt.merchant.external_id,
                            platform_merchant_name = receipt.merchant.name,

                            invoice_datetime = receiptDTO.invoice_datetime,

                            invoice_currency = receiptDTO.invoice_currency,
                            invoice_lines = receiptDTO.invoice_lines,
                            invoice_totals = receiptDTO.invoice_totals
                        )
                    )
                )

                # mark payment closed (bank has been notified)

                MerchantPosCallbackClient(
                    endpoint_from_url(receipt.merchant.callback_url)
                ).post(
                    PlatformReceiptMatchExternalNotification(
                        platform_receipt_id=receipt.external_id,
                        platform_client_ac_id=platform_bank_client_ac.external_id
                    )
                )

                # mark receipt as closed (merchant has been notified)

def before_launching_platform_matching_rest_server(config: ServiceConfig):

    def launch_match_job():
        match_job(config)

    schedule.every(JOB_PERIOD_S).seconds.do(launch_match_job)

    while True:
        schedule.run_pending()
        time.sleep(WAIT_PERIOD_S)
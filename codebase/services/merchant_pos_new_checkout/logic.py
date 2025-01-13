import datetime
import uuid
from model.orm.query import insert_all, insert_one, select_all
from model.write_model.objects.common import Currency
from model.write_model.objects.merchant_write_model import SKU, Invoice, InvoiceLine, InvoicePayment, PaymentProcessor
from services.merchant_pos_new_checkout.calc import new_merchant_invoice
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.platform_new_receipt.rqrsp import PlatformNewReceiptRequest
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import serialize_datetime


def handle_merchant_pos_new_checkout_request(
    config: ServiceConfig, 
    rq: MerchantPosNewCheckoutRequest
):
    
    db_engine = config.write_model_db_engine()

    currencies: list[Currency] = select_all(Currency, db_engine)
    def currency_for_iso3(iso3: str) -> Currency:
        return [c for c in currencies if c.iso3 == rq.currency][0]

    skus: list[SKU] = select_all(SKU, db_engine)

    # create invoice (with line items) from request

    currency = currency_for_iso3(rq.currency)

    lines = []

    for item in rq.items:

        sku = [x for x in skus if x.id == item.sku_id][0]

        lines.append(InvoiceLine(
            sku = sku,
            sku_count = item.sku_count,
            currency_amount = sku.price * item.sku_count
        ))

    invoice_timestamp = datetime.datetime.now()

    invoice = new_merchant_invoice(currency, invoice_timestamp, lines)

    # insert invoice

    persisted_invoice = insert_one(invoice, db_engine)

    # link and insert invoice lines

    for line in lines:
        line.invoice = persisted_invoice
        line.invoice_id = persisted_invoice.id

    insert_all(lines, db_engine)
    
    # trigger customer payment via payment processor

    unique_payment_reference = str(uuid.uuid4())

    payment_processor: PaymentProcessor = select_all(PaymentProcessor, db_engine)[0]

    # TODO client for specific payment processor
    pmt_proc_rsp: PaymentProcessorNewPaymentResponse = PaymentProcessorNewPaymentClient().post(
        PaymentProcessorNewPaymentRequest(
            currency=currency.iso3,
            currency_amt=invoice.total_amount_after_tax,

            invoice_timestamp=serialize_datetime(invoice_timestamp),
            reference=unique_payment_reference
    ))

    # failure case

    if not pmt_proc_rsp.successful:
        return MerchantPosNewCheckoutResponse(
            successful=False
        )
    
    # bad match case

    if pmt_proc_rsp.original_merchant_reference != unique_payment_reference:
        return MerchantPosNewCheckoutResponse(
            successful=False
        )

    # create payment and link to invoice

    payment = InvoicePayment(

        invoice = invoice,

        currency = currency,
        currency_amount = invoice.total_amount_after_tax,

        payment_processor = payment_processor,
        payment_processor_reference = pmt_proc_rsp.reference,

        successful = pmt_proc_rsp.successful,
        timestamp =  datetime.datetime.fromisoformat(pmt_proc_rsp.timestamp)
    )

    insert_one(payment, db_engine=db_engine)

    # TODO create receipt for submission to platform

    platform_receipt_rsp = PlatformNewReceiptClient().post(
        PlatformNewReceiptRequest(
        )
    )

    return MerchantPosNewCheckoutResponse(
        successful=payment.successful
    )

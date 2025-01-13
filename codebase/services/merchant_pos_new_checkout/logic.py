import datetime
import uuid
from model.orm.query import insert_all, insert_one, select_all
from model.write_model.objects.common import Currency
from model.write_model.objects.merchant_write_model import SKU, Invoice, InvoiceLine, InvoicePayment, InvoiceReceipt, PaymentProcessor
from services.merchant_pos_new_checkout.calc import new_merchant_invoice
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.platform_new_receipt.rqrsp import PlatformPaymentChannelEnum, PlatformPaymentChannelPaymentData, PlatformReceiptLine, PlatformReceiptRequest, PlatformReceiptTotals
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import deserialize_datetime, serialize_datetime, serialize_uuid


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

    # create and insert invoice

    invoice: Invoice = insert_one(
        new_merchant_invoice(currency, invoice_timestamp, lines), 
        db_engine
    )

    # link and insert invoice lines

    for line in lines:
        line.invoice = invoice
        line.invoice_id = invoice.id

    insert_all(lines, db_engine)
    
    # trigger customer payment via payment processor

    merchant_unique_payment_reference = uuid.uuid4()

    payment_processor: PaymentProcessor = select_all(PaymentProcessor, db_engine)[0]

    # TODO client for specific payment processor
    pmt_proc_rsp: PaymentProcessorNewPaymentResponse = PaymentProcessorNewPaymentClient().post(
        PaymentProcessorNewPaymentRequest(
            currency=currency.iso3,
            currency_amt=invoice.total_amount_after_tax,

            invoice_timestamp=serialize_datetime(invoice_timestamp),
            reference=serialize_uuid(merchant_unique_payment_reference)
    ))

    # failure case

    if not pmt_proc_rsp.successful:
        return MerchantPosNewCheckoutResponse(
            successful=False
        )
    
    # bad match case

    if pmt_proc_rsp.original_merchant_reference != serialize_uuid(merchant_unique_payment_reference):
        return MerchantPosNewCheckoutResponse(
            successful=False
        )

    # create payment and link to invoice

    payment = insert_one(
        InvoicePayment(

            invoice = invoice,

            currency = currency,
            currency_amount = invoice.total_amount_after_tax,

            payment_processor = payment_processor,
            payment_processor_reference = pmt_proc_rsp.reference,

            successful = pmt_proc_rsp.successful,
            timestamp =  deserialize_datetime(pmt_proc_rsp.timestamp)
        ), 
        db_engine=db_engine
    )

    # create receipt and link to invoice

    receipt: InvoiceReceipt = insert_one(
        InvoiceReceipt(
            invoice = invoice,
            invoice_id = invoice.id
        ), 
        db_engine=db_engine
    )

    platform_receipt_rq = PlatformReceiptRequest(
        merchant_reference = str(receipt.id),
        invoice_datetime = serialize_datetime(invoice_timestamp),
        invoice_currency = invoice.currency.iso3,
        invoice_lines = [PlatformReceiptLine(
            description=line.sku.name,
            count=line.sku_count,
            total_amount=line.currency_amount*line.sku_count
        ) for line in invoice.lines],
        invoice_totals = PlatformReceiptTotals(
            total_amount_before_tax = invoice.total_amount_before_tax,
            sales_tax_amount = invoice.sales_tax_amount,
            total_amount_after_tax = invoice.total_amount_after_tax
        ),
        payment_channel_payment_data = PlatformPaymentChannelPaymentData(
            payment_channel=PlatformPaymentChannelEnum.CARD.value,
            payment_channel_payment_reference=pmt_proc_rsp.reference
        )
    )

    platform_receipt_rsp = PlatformNewReceiptClient().post(
        platform_receipt_rq
    )

    return MerchantPosNewCheckoutResponse(
        successful=payment.successful
    )

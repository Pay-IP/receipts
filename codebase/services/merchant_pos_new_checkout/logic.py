import datetime
import uuid
from model.orm.query import insert_all, insert_one, select_all, select_on_filters, select_on_id
from model.write_model.objects.common import Currency
from model.write_model.objects.merchant_write_model import SKU, Invoice, InvoiceLine, InvoicePayment, InvoiceReceipt, PaymentProcessor
from services.merchant_pos_new_checkout.calc import new_merchant_invoice
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutRequestItem, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.platform_new_receipt.rqrsp import PlatformPaymentChannelEnum, PlatformPaymentChannelPaymentData, PlatformReceiptLine, PlatformReceiptRequest, PlatformReceiptTotals
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import deserialize_datetime, serialize_datetime, serialize_uuid


def construct_and_persist_core_invoice(
    db_engine,
    currency_str: str,
    items: list[MerchantPosNewCheckoutRequestItem]
) -> Invoice:

    currencies: list[Currency] = select_all(Currency, db_engine)
    
    def currency_for_iso3(iso3: str) -> Currency:
        return [c for c in currencies if c.iso3 == currency_str][0]

    skus: list[SKU] = select_all(SKU, db_engine)

    # create invoice (with line items) from request

    currency = currency_for_iso3(currency_str)

    lines = []

    for item in items:

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

    return invoice

def execute_customer_payment_via_payment_processor(
    db_engine, 
    invoice: Invoice, 
    payment_processor: PaymentProcessor
):

    merchant_unique_payment_reference = uuid.uuid4()

    pmt_proc_rsp: PaymentProcessorNewPaymentResponse = PaymentProcessorNewPaymentClient().post(
        PaymentProcessorNewPaymentRequest(
            currency=invoice.currency.iso3,
            currency_amt=invoice.total_amount_after_tax,
            invoice_timestamp=serialize_datetime(invoice.timestamp),
            reference=serialize_uuid(merchant_unique_payment_reference)
    ))

    # failure cases

    if pmt_proc_rsp.original_merchant_reference != serialize_uuid(merchant_unique_payment_reference):
        return False

    if not pmt_proc_rsp.successful:
        return False

    # create payment and link to invoice

    return insert_one(
        InvoicePayment(

            invoice = invoice,

            currency = invoice.currency,
            currency_amount = invoice.total_amount_after_tax,

            payment_processor = payment_processor,
            payment_processor_reference = pmt_proc_rsp.reference,

            successful = pmt_proc_rsp.successful,
            timestamp =  deserialize_datetime(pmt_proc_rsp.timestamp)
        ), 
        db_engine
    )

def create_receipt_for_invoice_and_submit_to_platform(
    db_engine, 
    invoice_id: int
):
    
    invoice: Invoice = select_on_id(db_engine, Invoice, invoice_id)

    receipt: InvoiceReceipt = insert_one(
        InvoiceReceipt(
            # invoice = invoice,
            invoice_id = invoice.id
        ), 
        db_engine=db_engine
    )

    payment_matching_criteria = { 'invoice_id': invoice.id, 'successful': True }
    
    payments: list[InvoicePayment] = select_on_filters(db_engine, InvoicePayment, payment_matching_criteria)
    successful_payment_count = len(payments)
    if successful_payment_count != 1:
        raise Exception(f'in order to generate a receipt, invoice {invoice_id} must have exactly one successful payment, not {successful_payment_count}')
    
    payment = payments[0]

    platform_receipt_rq = PlatformReceiptRequest(
        merchant_reference = str(receipt.id),
        invoice_datetime = serialize_datetime(invoice.timestamp),
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
            payment_channel_payment_reference=payment.payment_processor_reference
        )
    )

    platform_receipt_rsp = PlatformNewReceiptClient().post(
        platform_receipt_rq
    )


def handle_merchant_pos_new_checkout_request(
    config: ServiceConfig, 
    rq: MerchantPosNewCheckoutRequest
):
    
    db_engine = config.write_model_db_engine()
    invoice = construct_and_persist_core_invoice(db_engine, rq.currency, rq.items)

    payment_processor: PaymentProcessor = select_all(PaymentProcessor, db_engine)[0]
    customer_payment = execute_customer_payment_via_payment_processor(db_engine, invoice, payment_processor)
    customer_payment_was_successful = customer_payment.successful
    create_receipt_for_invoice_and_submit_to_platform(db_engine, invoice.id)

    return MerchantPosNewCheckoutResponse(
        successful=customer_payment_was_successful
    )

import datetime
import uuid
from model.query import insert_all, insert_one, select_all, select_all_on_filters, select_on_id, update_existing
from model.write_model.objects.currency import Currency
from model.write_model.objects.emv import TerminalEmvReceipt, mask_pan
from model.write_model.objects.merchant_write_model import SKU, Invoice, InvoiceLine, InvoicePayment, InvoiceReceipt, PaymentProcessor
from model.write_model.objects.platform_common import PlatformEmvReceipt, PlatformMerchantReceiptDTO, PlatformReceiptLine, PlatformReceiptTotals
from services.merchant_pos_new_checkout.calc import new_merchant_invoice
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutRequestItem, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewCardPaymentResponse
from util.service.service_config_base import ServiceConfig
from util.web import serialize_datetime, serialize_uuid

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

def execute_invoice_payment(
    db_engine, 
    invoice: Invoice
) -> InvoicePayment:
    
    payment_processor: PaymentProcessor = select_all(PaymentProcessor, db_engine)[0]

    merchant_unique_payment_reference = uuid.uuid4()

    pmt_proc_rsp: PaymentProcessorNewCardPaymentResponse = PaymentProcessorNewPaymentClient().new_card_payment(
        currency=invoice.currency.iso3,
        currency_amt=invoice.total_amount_after_tax,
        timestamp=invoice.timestamp,
        reference=serialize_uuid(merchant_unique_payment_reference)
    )

    if not pmt_proc_rsp.successful:
        # TODO basic handling
        return None

    # create payment and link to invoice

    return insert_one(
        InvoicePayment(

            invoice_id = invoice.id,
            successful = pmt_proc_rsp.successful,
            timestamp = datetime.datetime.now(),

            # TODO confirm against rsp
            currency = invoice.currency,
            currency_amount = invoice.total_amount_after_tax,

            payment_processor = payment_processor,
            payment_processor_reference = pmt_proc_rsp.payment_processor_payment_reference,

            terminal_emv_receipt = pmt_proc_rsp.terminal_emv_receipt.model_dump_json()
        ), 
        db_engine
    )

def platform_emv_receipt_from_terminal_emv_receipt(
    terminal_emv_receipt: TerminalEmvReceipt
) -> PlatformEmvReceipt:
    
    return PlatformEmvReceipt(
        merchant_address = terminal_emv_receipt.iso.rq.merchant_address,

        transaction_date_str = terminal_emv_receipt.iso.rq.transaction_date_str,
        transaction_time_str = terminal_emv_receipt.iso.rq.transaction_time_str,

        authorized = terminal_emv_receipt.iso.rsp.authorized,

        masked_pan = mask_pan(terminal_emv_receipt.iso.rq.pan),
        terminal_serial_number = terminal_emv_receipt.iso.rq.terminal_serial_number,
        retrieval_reference_number = terminal_emv_receipt.iso.rq.retrieval_reference_number,
        authorization_response_identifier = terminal_emv_receipt.iso.rsp.authorization_response_identifier,
        emv_application_label = terminal_emv_receipt.iso.rq.emv_application_label,

        unique_transaction_identifier = terminal_emv_receipt.iso.rq.unique_transaction_identifier,

        currency_code = terminal_emv_receipt.iso.rq.currency_code,
        currency_amount = terminal_emv_receipt.iso.rq.currency_amount,

        application_ID = terminal_emv_receipt.iso.rq.application_ID,
        CTQ = terminal_emv_receipt.iso.rq.CTQ,
        terminal_verification_results = terminal_emv_receipt.iso.rq.terminal_verification_results,
        application_cryptogram = terminal_emv_receipt.iso.rq.application_cryptogram

    )

def create_receipt_for_invoice_and_submit_to_platform(
    db_engine, 
    invoice_id: int
):
    
    invoice: Invoice = select_on_id(Invoice, invoice_id, db_engine)

    receipt: InvoiceReceipt = insert_one(
        InvoiceReceipt(
            invoice_id = invoice.id,
            external_id = uuid.uuid4()
        ), 
        db_engine=db_engine
    )

    successful_payments: list[InvoicePayment] = select_all_on_filters(
        InvoicePayment, 
        { 'invoice_id': invoice.id, 'successful': True }, 
        db_engine
    )
    successful_payment_count = len(successful_payments)
    if successful_payment_count != 1:
        raise Exception(f'in order to generate a receipt, invoice {invoice_id} must have exactly one successful payment, not {successful_payment_count}')
    
    payment = successful_payments[0]

    terminal_emv_receipt = TerminalEmvReceipt.parse_raw(payment.terminal_emv_receipt)

    platform_emv_receipt = platform_emv_receipt_from_terminal_emv_receipt(terminal_emv_receipt)

    platform_receipt_rq = PlatformMerchantReceiptDTO(
        merchant_receipt_id = receipt.external_id,
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
        emv_receipt=platform_emv_receipt
    )

    platform_receipt_rsp = PlatformNewReceiptClient().post(
        platform_receipt_rq
    )

    receipt.platform_receipt_id = platform_receipt_rsp.platform_receipt_id
    update_existing(receipt, db_engine)

    return True

def handle_merchant_pos_new_checkout_request(
        
    config: ServiceConfig, 
    rq: MerchantPosNewCheckoutRequest
):
    
    db_engine = config.write_model_db_engine()

    invoice = construct_and_persist_core_invoice(db_engine, rq.currency, rq.items)
    invoice_payment = execute_invoice_payment(db_engine, invoice)
    create_receipt_for_invoice_and_submit_to_platform(db_engine, invoice.id)

    return MerchantPosNewCheckoutResponse(
        successful=invoice_payment.successful
    )

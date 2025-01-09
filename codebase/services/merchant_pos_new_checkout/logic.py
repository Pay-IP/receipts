import datetime
from decimal import Decimal
from model.object_model.query.select import insert_all, insert_one, select_all
from model.object_model.write_model.common import Currency
from model.object_model.write_model.merchant_write_model import SKU, Invoice, InvoiceLine, InvoicePayment, PaymentProcessor
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutResponse
from services.platform_new_receipt.client import PlatformNewReceiptClient
from services.platform_new_receipt.rqrsp import PlatformNewReceiptRequest
from services.pmt_proc_new_pmt.client import PaymentProcessorNewPaymentClient
from services.pmt_proc_new_pmt.rqrsp import PaymentProcessorNewPaymentRequest, PaymentProcessorNewPaymentResponse
from util.service.service_config_base import ServiceConfig


# merchant seed data required
# - currency
# - payment processor
# - SKUs

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

    sales_tax_percent = Decimal('14.0') # TODO source from DB
    total_amount_before_tax = sum([line.currency_amount for line in lines])
    sales_tax_amount = total_amount_before_tax * sales_tax_percent / Decimal('100.0')

    invoice = Invoice(

        timestamp = datetime.datetime.now(),

        currency = currency,
        sales_tax_percent = sales_tax_percent, 

        total_amount_before_tax = total_amount_before_tax,
        sales_tax_amount = sales_tax_amount,
        total_amount_after_tax = total_amount_before_tax - sales_tax_amount
    )

    invoice_id = insert_one(invoice, db_engine=db_engine)

    for line in lines:
        line.invoice = invoice_id

    insert_all(lines, db_engine)
        
    # with Session(db_engine) as db_session:
    #     with db_session.begin():            
            
    #         for item in items:            
    #             db_session.add(item)
            
    #         db_session.flush()


    # trigger customer payment via payment processor

    payment_processor: PaymentProcessor = select_all(PaymentProcessor, db_engine)[0]

    # TODO client for payment processor
    pmt_proc_rsp: PaymentProcessorNewPaymentResponse = PaymentProcessorNewPaymentClient().post(
        PaymentProcessorNewPaymentRequest(
            currency=currency.iso3,
            currency_amt=invoice.total_amount_after_tax
    ))

    # create an invoice payment

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

    platform_receipt = PlatformNewReceiptClient().post(
        PlatformNewReceiptRequest(
        )
    )

    return MerchantPosNewCheckoutResponse(
        successful=payment.successful
    )

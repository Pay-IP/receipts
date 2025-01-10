

import datetime
from decimal import Decimal
from model.write_model.objects.common import Currency
from model.write_model.objects.merchant_write_model import Invoice, InvoiceLine


def applicable_sales_tax_percent(
    currency: Currency, # should be country code
    timestamp: datetime.datetime
) -> Decimal:

    # TODO model and source from database
    #
    match currency.iso3, timestamp:
        case 'USD', _:
            return Decimal('6.0') # DC
        case 'EUR', _:
            return Decimal('21.50')
        case 'GBP', _:
            return Decimal('20.0')
        case 'ZAR', _:
            return Decimal('15.0')
        case 'BTC', _:
            return Decimal('0.0')
        
    raise Exception(f'Unsupported currency: {currency.iso3}')

def new_merchant_invoice(
    currency: Currency, 
    timestamp: datetime.datetime,
    invoice_lines: list[InvoiceLine],
) -> None:

    sales_tax_percent = applicable_sales_tax_percent(currency, timestamp)

    total_amount_before_tax = sum([line.currency_amount for line in invoice_lines])
    sales_tax_amount = total_amount_before_tax * sales_tax_percent / Decimal('100.0')
    total_amount_after_tax = total_amount_before_tax + sales_tax_amount 

    return Invoice(

        timestamp = timestamp,
        
        currency = currency,
        sales_tax_percent = sales_tax_percent,

        total_amount_before_tax = total_amount_before_tax,
        sales_tax_amount = sales_tax_amount,
        total_amount_after_tax = total_amount_after_tax
    )
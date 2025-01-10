from sqlalchemy import Column, Integer, DateTime, String, SMALLINT, DECIMAL, Boolean
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from model.write_model.objects.write_model_base import WriteModelBase

class MerchantClient(WriteModelBase):
    __tablename__ = 'merchant_client'

    id = Column(Integer, primary_key=True)
    platform_id = Column(UUID(as_uuid=True), nullable=False)
    

class PaymentProcessor(WriteModelBase):
    __tablename__ = 'merchant_payment_processor'

    id = Column(Integer, primary_key=True)
    name = Column(String(254), unique=True, nullable=False)
    vostro_id = Column(UUID(as_uuid=True), nullable=False)

class SKU(WriteModelBase):
    __tablename__ = 'merchant_sku'

    id = Column(Integer, primary_key=True)
    name = Column(String(254), nullable=False)
    price = Column(Integer, nullable=False)

class Invoice(WriteModelBase):
    __tablename__ = 'merchant_invoice'
    
    id = Column(Integer, primary_key=True)
    client = Column('client_id', ForeignKey('merchant_client.id'), nullable=True)

    timestamp = Column(DateTime(timezone=True), nullable=False) 
    
    currency = Column('currency_id', ForeignKey('currency.id'), nullable=False)
    sales_tax_percent = Column(DECIMAL(10, 2), nullable=False)
    
    total_amount_before_tax = Column(Integer())
    sales_tax_amount = Column(Integer())
    total_amount_after_tax = Column(Integer())

class InvoiceLine(WriteModelBase):
    __tablename__ = 'merchant_invoice_line'

    id = Column(Integer, primary_key=True)
    invoice = Column('invoice_id', ForeignKey('merchant_invoice.id'), nullable=False)

    sku = Column('sku_id', ForeignKey('merchant_sku.id'), nullable=False)
    sku_count = Column(Integer, nullable=False)
    
    currency_amount = Column(Integer, nullable=False)

class InvoicePayment(WriteModelBase):
    __tablename__ = 'merchant_invoice_payment'

    id = Column(Integer, primary_key=True)
    invoice = Column('invoice_id', ForeignKey('merchant_invoice.id'), nullable=False)

    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) 
   
    currency = Column('currency_id', ForeignKey('currency.id'), nullable=False)
    currency_amount = Column(Integer, nullable=False)

    payment_processor = Column('payment_processor_id', ForeignKey('merchant_payment_processor.id'), nullable=False)
    payment_processor_reference = Column(String(254), nullable=False)

    successful = Column(Boolean, unique=False, default=False, nullable=False)

class InvoiceReceipt(WriteModelBase):
    __tablename__ = 'merchant_invoice_receipt'

    id = Column(Integer, primary_key=True)
    invoice = Column('invoice_id', ForeignKey('merchant_invoice.id'), nullable=False)
    

from psycopg2.extensions import register_adapter, AsIs
for fk_class in [MerchantClient, PaymentProcessor, SKU, Invoice]:
    register_adapter(fk_class, lambda x: AsIs(f"'{x.id}'"))
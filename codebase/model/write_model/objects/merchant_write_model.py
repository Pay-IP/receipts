from sqlalchemy import Column, Integer, DateTime, String, SMALLINT, DECIMAL, Boolean
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from model.write_model.objects.write_model_base import WriteModelBase

class MerchantClient(WriteModelBase):
    __tablename__ = 'merchant_client'

    id = Column(Integer, primary_key=True)
    platform_reference = Column(UUID(as_uuid=True), nullable=False)
    
class PaymentProcessor(WriteModelBase):
    __tablename__ = 'merchant_payment_processor'

    id = Column(Integer, primary_key=True)
    name = Column(String(254), unique=True, nullable=False)
    merchant_reference = Column(UUID(as_uuid=True), nullable=False)

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
    
    currency_id = Column('currency_id', ForeignKey('currency.id'), nullable=False)
    currency = relationship('Currency', lazy=False)
    
    sales_tax_percent = Column(DECIMAL(10, 2), nullable=False)
    total_amount_before_tax = Column(Integer())
    sales_tax_amount = Column(Integer())
    total_amount_after_tax = Column(Integer())

    lines = relationship('InvoiceLine', back_populates='invoice', lazy=False)
    payments = relationship('InvoicePayment', back_populates='invoice', lazy=False)
    receipts = relationship('InvoiceReceipt', back_populates='invoice', lazy=False)

class InvoiceLine(WriteModelBase):
    __tablename__ = 'merchant_invoice_line'

    id = Column(Integer, primary_key=True)

    invoice_id = Column('invoice_id', ForeignKey('merchant_invoice.id'), nullable=False)
    invoice = relationship("Invoice", back_populates="lines")

    sku_id = Column('sku_id', ForeignKey('merchant_sku.id'), nullable=False)
    sku = relationship('SKU', lazy=False)

    sku_count = Column(Integer, nullable=False)
    
    currency_amount = Column(Integer, nullable=False)

class InvoicePayment(WriteModelBase):
    __tablename__ = 'merchant_invoice_payment'

    id = Column(Integer, primary_key=True)

    invoice_id = Column('invoice_id', ForeignKey('merchant_invoice.id'), nullable=False)
    invoice = relationship("Invoice", back_populates="payments")

    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) 
   
    currency_id = Column('currency_id', ForeignKey('currency.id'), nullable=False)
    currency = relationship('Currency', lazy='select')

    currency_amount = Column(Integer, nullable=False)

    payment_processor_id = Column(
        'payment_processor_id', 
        ForeignKey('merchant_payment_processor.id'), 
        nullable=False
    )
    payment_processor = relationship('PaymentProcessor', lazy=False)
    payment_processor_reference = Column(String(254), nullable=False)

    terminal_emv_receipt = Column(String, nullable=False)

    successful = Column(Boolean, unique=False, default=False, nullable=False)

class InvoiceReceipt(WriteModelBase):
    __tablename__ = 'merchant_invoice_receipt'

    id = Column(Integer, primary_key=True)
    external_id = Column(UUID(as_uuid=True), nullable=False)
    
    invoice_id = Column('invoice_id', ForeignKey('merchant_invoice.id'), nullable=False)
    invoice = relationship("Invoice", back_populates="receipts")

from psycopg2.extensions import register_adapter, AsIs
for fk_class in [MerchantClient, PaymentProcessor, SKU, Invoice]:
    register_adapter(fk_class, lambda x: AsIs(f"'{x.id}'"))
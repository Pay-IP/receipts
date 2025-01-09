from sqlalchemy import Column, Integer, DateTime, String, SMALLINT
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from model.object_model.core.write_model_base import WriteModelBase

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
    client = Column(ForeignKey('merchant_client.id'), nullable=True)

    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) 
    
    currency = Column(String(3), nullable=False)
    
    total_amount_before_tax = Column(Integer())
    sales_tax_amount = Column(Integer())
    total_amount_after_tax = Column(Integer())

class InvoiceLine(WriteModelBase):
    __tablename__ = 'merchant_invoice_line'

    id = Column(Integer, primary_key=True)
    invoice = Column(ForeignKey('merchant_invoice.id'), nullable=False)

    sku = Column(ForeignKey('merchant_sku.id'), nullable=False)
    sku_count = Column(Integer, nullable=False)
    currency_amount = Column(Integer, nullable=False)

class InvoicePayment(WriteModelBase):
    __tablename__ = 'merchant_invoice_payment'

    id = Column(Integer, primary_key=True)
    invoice = Column(ForeignKey('merchant_invoice.id'), nullable=False)

    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) 
   
    currency = Column(String(3), nullable=False)
    currency_amount = Column(Integer, nullable=False)

    payment_processor = Column(ForeignKey('merchant_payment_processor.id'), nullable=False)
    payment_processor_reference = Column(String(254), nullable=False)

class InvoiceReceipt(WriteModelBase):
    __tablename__ = 'merchant_invoice_receipt'

    id = Column(Integer, primary_key=True)
    invoice = Column(ForeignKey('merchant_invoice.id'), nullable=False)
    
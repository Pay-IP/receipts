from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from model.write_model.objects.write_model_base import WriteModelBase
from model.write_model.objects.currency import Currency # DO NOT DELETE - this is required for the ORM

class PaymentProcessorMerchant(WriteModelBase):
    __tablename__ = 'payment_processor_merchant'

    id = Column(Integer, primary_key=True)

    currency_id = Column('currency_id', ForeignKey('currency.id'), nullable=False)
    currency = relationship('Currency', lazy=False)
    
    name = Column(String(254), nullable=False)
    address = Column(String, nullable=False)


class PaymentProcessorMerchantTSN(WriteModelBase):
    __tablename__ = 'payment_processor_merchant_tsn'

    tsn = Column(Integer, primary_key=True)

    merchant_id = Column('merchant_id', ForeignKey('payment_processor_merchant.id'), nullable=False)
    merchant = relationship('PaymentProcessorMerchant', lazy=False)

class PaymentProcessorSystemTraceAuditNumber(WriteModelBase):
    __tablename__ = 'payment_processor_system_trace_audit_number'
    stan = Column(Integer, primary_key=True)

class PaymentProcessorMerchantPayment(WriteModelBase):
    __tablename__ = 'payment_processor_merchant_payment'

    id = Column(Integer, primary_key=True)

    merchant_id = Column('merchant_id', ForeignKey('payment_processor_merchant.id'), nullable=False)
    merchant = relationship('PaymentProcessorMerchant', lazy=False)

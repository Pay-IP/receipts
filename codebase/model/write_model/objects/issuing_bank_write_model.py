from sqlalchemy import Column, Integer, DateTime, String, JSON, DATE
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from model.write_model.objects.write_model_base import WriteModelBase
from model.write_model.objects.currency import Currency # DO NOT DELETE - this is required by the ORM for the Currency FK reference

class IssuingBankClientAccount(WriteModelBase):
    __tablename__ = 'issuing_bank_client_account'

    id = Column(Integer, primary_key=True)

    name = Column(String(254), nullable=False)

    currency_id = Column('currency_id', ForeignKey('currency.id'), nullable=False)
    currency = relationship('Currency', lazy=False)

    external_id = Column(UUID(as_uuid=True), nullable=False)

    card_pan = Column(String(19), nullable=False)
    card_aid = Column(String(32), nullable=False)
    card_app_label = Column(String(20), nullable=False)

    date_of_birth = Column(DATE, nullable=False)
    postal_code = Column(String(254), nullable=False)

class IssuingBankClientAccountDebit(WriteModelBase):
    __tablename__ = 'issuing_bank_client_account_debit'

    id = Column(Integer, primary_key=True)    
    external_id = Column(UUID(as_uuid=True), nullable=False)
    platform_payment_id = Column(UUID(as_uuid=True), nullable=False)

    client_account_id = Column('client_account_id', ForeignKey('issuing_bank_client_account.id'), nullable=False)
    client_account = relationship('IssuingBankClientAccount', lazy=False)

    currency_amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False) 

    platform_receipt_id = Column(UUID(as_uuid=True), nullable=False)
    platform_receipt = Column(JSON, nullable=True)

    emv_rq = Column(JSON, nullable=False)
    emv_rsp = Column(JSON, nullable=False)
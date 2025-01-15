from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from model.write_model.objects.write_model_base import WriteModelBase

class IssuingBankClientAccount(WriteModelBase):
    __tablename__ = 'issuing_bank_client_account'

    id = Column(Integer, primary_key=True)

    name = Column(String(254), nullable=False)
    age = Column(Integer, nullable=False)

    currency_id = Column('currency_id', ForeignKey('currency.id'), nullable=False)
    currency = relationship('Currency', lazy=False)

    external_client_id = Column(UUID(as_uuid=True), nullable=False)
    external_account_id = Column(UUID(as_uuid=True), nullable=False)

    card_pan = Column(String(19), nullable=False)

class IssuingBankPlatformReceipt(WriteModelBase):
    __tablename__ = 'issuing_bank_platform_receipt'

    id = Column(Integer, primary_key=True)    
    
    platform_reference = Column(UUID(as_uuid=True), nullable=False)
    receipt_json = Column(String, nullable=False)

class IssuingBankClientAccountDebit(WriteModelBase):
    __tablename__ = 'issuing_bank_client_account_debit'

    id = Column(Integer, primary_key=True)    

    client_account_id = Column('client_account_id', ForeignKey('issuing_bank_client_account.id'), nullable=False)
    client_account = relationship('IssuingBankClientAccount', lazy=False)

    currency_amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False) 

    platform_receipt_id = Column('platform_receipt_id', ForeignKey('issuing_bank_platform_receipt.id'), nullable=True)
    platform_receipt = relationship('IssuingBankPlatformReceipt', lazy=False) 





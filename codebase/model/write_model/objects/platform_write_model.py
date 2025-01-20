from sqlalchemy import Column, Integer, DateTime, String, JSON
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from model.write_model.objects.write_model_base import WriteModelBase

# merchant data ---------------------------------------------------------------------------------


class PlatformMerchant(WriteModelBase):
    __tablename__ = 'platform_merchant'
    id = Column(Integer, primary_key=True)

    name = Column(String(254), nullable=False)

class PlatformMerchantConfig(WriteModelBase):
    __tablename__ = 'platform_merchant_config'
    id = Column(Integer, primary_key=True)

    merchant_id = Column('merchant_id', ForeignKey('platform_merchant.id'), nullable=False)
    merchant = relationship('PlatformMerchant', lazy=False)

    merchant_address = Column(String(254), nullable=False)
    merchant_categorisation_code = Column(String(4), nullable=False)

# bank ------------------------------------------------------------------------------------------

class PlatformBank(WriteModelBase):
    __tablename__ = 'platform_bank'
    id = Column(Integer, primary_key=True)
    
    name = Column(String(254), nullable=False)

class PlatformBankConfig(WriteModelBase):
    __tablename__ = 'platform_bank_config'
    id = Column(Integer, primary_key=True)

    bank_id = Column('bank_id', ForeignKey('platform_bank.id'), nullable=False)
    bank = relationship('PlatformBank', lazy=False)

    card_bin = Column(String(6), nullable=False)

# bank client account ---------------------------------------------------------------------------

class PlatformBankClientAccount(WriteModelBase):
    __tablename__ = 'platform_bank_client_ac'
    id = Column(Integer, primary_key=True)

    bank_id = Column('bank_id', ForeignKey('platform_bank.id'), nullable=False)
    bank = relationship('PlatformBank', lazy=False)

    source_system_id = Column(UUID(as_uuid=True), nullable=False)

class PlatformBankClientAccountMetaData(WriteModelBase):
    __tablename__ = 'platform_bank_client_ac_meta_data'
    id = Column(Integer, primary_key=True)

    bank_client_ac_id = Column('bank_client_ac_id', ForeignKey('platform_bank_client_ac.id'), nullable=False)
    bank_client_ac = relationship('PlatformBankClientAccount', lazy=False)

    client_age = Column(Integer, nullable=False)
    client_postal_code = Column(String(254), nullable=False)

# payments and receipts  ------------------------------------------------------------------------

class PlatformBankClientAccountPayment(WriteModelBase):
    __tablename__ = 'platform_bank_client_ac_payment'
    id = Column(Integer, primary_key=True)

    bank_client_ac_id = Column('bank_client_ac_id', ForeignKey('platform_bank_client_ac.id'), nullable=False)
    bank_client_ac = relationship('PlatformBankClientAccount', lazy=False)

    system_timestamp = Column(DateTime(timezone=True), nullable=False)
    source_system_id = Column(UUID(as_uuid=True), nullable=False)

    payment = Column(JSON, nullable=False)

class PlatformMerchantReceipt(WriteModelBase):
    __tablename__ = 'platform_merchant_receipt'

    id = Column(Integer, primary_key=True)
    external_id = Column(UUID(as_uuid=True), nullable=False)
    source_system_id = Column(UUID(as_uuid=True), nullable=False)

    merchant_id = Column('merchant_id', ForeignKey('platform_merchant.id'), nullable=False)
    merchant = relationship('PlatformMerchant', lazy=False)

    system_timestamp = Column(DateTime(timezone=True), nullable=False)
    receipt = Column(JSON, nullable=False)

class PlatformMatchMerchantReceiptToBankClientAccountPayment(WriteModelBase):
    __tablename__ = 'platfrm_match_merchant_receipt_to_bank_client_ac_payment'
    
    id = Column(Integer, primary_key=True)

    merchant_receipt_id = Column('merchant_receipt_id', ForeignKey('platform_merchant_receipt.id'), nullable=False)
    merchant_receipt = relationship('PlatformMerchantReceipt', lazy=False)

    bank_client_ac_payment_id = Column('bank_client_ac_payment_id', ForeignKey('platform_bank_client_ac_payment.id'), nullable=False)
    bank_client_ac_payment = relationship('PlatformBankClientAccountPayment', lazy=False)

    timestamp = Column(DateTime(timezone=True), nullable=False)
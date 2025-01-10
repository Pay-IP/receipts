from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DECIMAL
from sqlalchemy.dialects.postgresql import UUID

from model.write_model.objects.write_model_base import WriteModelBase

class BuyOrderRunningTotal(WriteModelBase):
    __tablename__ = 'buy_order_running_total'
    id = Column(Integer, primary_key=True)
    btc_amount  = Column(DECIMAL(precision=12, scale=8), nullable=False)

class BuyOrder(WriteModelBase):
    __tablename__ = 'buy_order'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('client.id'), nullable=False)
    external_id = Column(UUID(as_uuid=True), nullable=False, server_default=text('gen_random_uuid()'))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) 

    currency_id = Column(ForeignKey('currency.id'), nullable=False)
    currency_amount = Column(DECIMAL(precision=12, scale=2), nullable=False)
    btc_rate = Column(DECIMAL(precision=12, scale=2), nullable=False)
    btc_amount  = Column(DECIMAL(precision=11, scale=8), nullable=False)

class BuyOrderIdempotenceCache(WriteModelBase):
    __tablename__ = 'buy_order_idempotence_cache'

    client_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=False)
    currency_amount = Column(DECIMAL(precision=12, scale=2), nullable=False)
    idempotence_key = Column(UUID(as_uuid=True), nullable=False)

    buy_order_id = Column(Integer, primary_key=True)



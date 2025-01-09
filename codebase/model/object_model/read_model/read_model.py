from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql.sqltypes import DECIMAL, String
from sqlalchemy.dialects.postgresql import UUID

from model.object_model.core.read_model_base import ReadModelBase

class BuyOrderReadModel(ReadModelBase):
    __tablename__ = 'buy_order_read_model'

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    client_id = Column(Integer, nullable=False)
    external_id = Column(UUID(as_uuid=True), nullable=False)
    currency_id = Column(Integer, nullable=False)
    currency_iso3 = Column(String(3), nullable=False)

    currency_amount = Column(DECIMAL(precision=12, scale=2), nullable=False)
    btc_rate = Column(DECIMAL(precision=12, scale=2), nullable=False)
    btc_amount  = Column(DECIMAL(precision=11, scale=8), nullable=False)
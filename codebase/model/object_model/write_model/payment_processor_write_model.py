# Merchant
# - id
# - name
# - URL

# IssuingBank
# - id
# - name
# - URL

# Transaction
# - id
# - timestamp
# - merchant_id
# - issuing_bank_id
# - total
# - currency
# - reference


from sqlalchemy import Column, Integer, DateTime, String, SMALLINT
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from model.object_model.core.write_model_base import WriteModelBase

class Currency(WriteModelBase):
    __tablename__ = 'pmt_proc_currency'

    id = Column(Integer, primary_key=True)
    iso3 = Column(String(3), nullable=False)
    decimal_places = Column(SMALLINT, nullable=False)

    def __repr__(self):
       return f'id {self.id}: {self.iso3} ({self.decimal_places} decimal places)'

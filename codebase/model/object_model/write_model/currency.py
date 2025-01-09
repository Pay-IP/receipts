from sqlalchemy import Column, Integer, String, SMALLINT

from model.object_model.core.write_model_base import WriteModelBase

class Currency(WriteModelBase):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    iso3 = Column(String(3), nullable=False)
    dp = Column(SMALLINT, nullable=False)

    def __repr__(self):
       return f'id {self.id}: {self.iso3} ({self.dp} DP)'
    

from model.object_model.common import SUPPORTED_CURRENCIES

supported_currencies = ",".join([f'"{x}"' for x in SUPPORTED_CURRENCIES])
from sqlalchemy import Column, Integer, String, SMALLINT

from model.object_model.core.write_model_base import WriteModelBase

class Currency(WriteModelBase):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    iso3 = Column(String(3), nullable=False)
    decimal_places = Column(SMALLINT, nullable=False)

    def __repr__(self):
       return f'id {self.id}: {self.iso3} ({self.decimal_places} DP)'

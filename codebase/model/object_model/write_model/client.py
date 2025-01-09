from sqlalchemy import Column, Integer, String

from model.object_model.core.write_model_base import WriteModelBase

class Client(WriteModelBase):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    email = Column(String(254), unique=True, nullable=False)

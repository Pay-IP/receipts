import uuid
from model.write_model.objects.merchant_write_model import SKU, PaymentProcessor
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from util.web import serialize_uuid

#from model.object_model.write_model.merchant_write_model import SKU, PaymentProcessor

def seed_merchant_skus(db_engine: Engine):

    seed_skus = [
        SKU(name="espresso", price=3000),
        SKU(name="filter coffee", price=3500),
        SKU(name="cuppacino", price=4300),
        SKU(name="swiss coffee", price=4800),
    ]

    with Session(db_engine) as db_session:
        with db_session.begin():            

            existing_skus = db_session.execute(
                select(SKU)
            ).scalars().all()

            for sku in seed_skus:
                if len([sku for sku in existing_skus if sku.name == sku.name]) == 0:
                    db_session.add(sku)
            
            db_session.flush()

def seed_merchant_payment_processors(db_engine: Engine):

    payment_processors = [
        PaymentProcessor(
            name = 'Nedbank',
            merchant_reference = serialize_uuid(uuid.uuid4())
        ),
    ]

    with Session(db_engine) as db_session:
        with db_session.begin():            

            existing_processors = db_session.execute(
                select(PaymentProcessor)
            ).scalars().all()

            for processor in payment_processors:
                if len([processor for processor in existing_processors if processor.name == processor.name]) == 0:
                    db_session.add(processor)
            
            db_session.flush()


def seed_merchant_write_model(db_engine: Engine):

    seed_merchant_skus(db_engine)
    seed_merchant_payment_processors(db_engine)
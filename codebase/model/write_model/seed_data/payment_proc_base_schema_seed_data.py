import random
import uuid
from model.write_model.objects.currency import Currency
from model.write_model.objects.payment_processor_write_model import PaymentProcessorMerchant
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

def seed_payment_processor_merchants(db_engine: Engine):

    with Session(db_engine) as db_session:
        with db_session.begin():         

            existing_currencies = db_session.execute(
                select(Currency)
            ).scalars().all()

            currency = random.sample(existing_currencies, 1)[0]

            seed_merchants = [
                PaymentProcessorMerchant(
                    currency_id = currency.id,
                    name = 'Mr Price',
                    address = 'Mr Price Clothing',
                ),
            ]

            existing_merchants = db_session.execute(
                select(PaymentProcessorMerchant)
            ).scalars().all()

            for seed_merchant in seed_merchants:
                if len([existing_merchant for existing_merchant in existing_merchants if existing_merchant.name == seed_merchant.name]) == 0:
                    db_session.add(seed_merchant)
            
            db_session.flush()


def seed_payment_processor_base_schema(db_engine: Engine):
    seed_payment_processor_merchants(db_engine)
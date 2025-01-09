from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from model.object_model.write_model.merchant_write_model import SKU, Currency

def seed_merchant_write_model_data(db_engine: Engine):
    seed_currencies = [
        Currency(iso3='BTC', decimal_places=8),
        Currency(iso3='EUR', decimal_places=2),
        Currency(iso3='GBP', decimal_places=2),
        Currency(iso3='USD', decimal_places=2),
        Currency(iso3='ZAR', decimal_places=2),
    ]

    seed_skus = [
        SKU(name="espresso", price=3000),
        SKU(name="filter coffee", price=3500),
        SKU(name="cuppacino", price=4300),
        SKU(name="swiss coffee", price=4800),
    ]

    with Session(db_engine) as db_session:

        with db_session.begin():            

            # Currencies

            existing_currencies = db_session.execute(
                select(Currency)
            ).scalars().all()

            for currency in seed_currencies:
                if len([x for x in existing_currencies if x.iso3 == currency.iso3]) == 0:
                    db_session.add(currency)

            db_session.flush()

            # SKUs

            existing_skus = db_session.execute(
                select(SKU)
            ).scalars().all()

            for sku in seed_skus:
                if len([sku for sku in existing_skus if sku.name == sku.name]) == 0:
                    db_session.add(sku)
            
            db_session.flush()

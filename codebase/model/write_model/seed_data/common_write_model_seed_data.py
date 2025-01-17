from model.write_model.objects.currency import Currency
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select


def seed_common_write_model(db_engine: Engine):
   
    seed_currencies = [
        # Currency(iso3='BTC', decimal_places=8),
        # Currency(iso3='EUR', decimal_places=2),
        # Currency(iso3='GBP', decimal_places=2),
        # Currency(iso3='USD', decimal_places=2),
        Currency(iso3='ZAR', decimal_places=2, symbol='R'),
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
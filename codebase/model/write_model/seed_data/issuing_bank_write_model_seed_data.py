import random
import uuid
from model.orm.query import select_all_on_filters, select_first_on_filters
from model.write_model.objects.currency import Currency
from model.write_model.objects.emv import random_card_pan_for_bin
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccount
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
import datetime

def seed_issuing_bank_client_accounts(db_engine: Engine):

    min_age = 18
    max_age = 65
    
    bin = '484795'
    aid = 'A0000000031010'
    application_label = 'Visa Debit'

    currency = select_first_on_filters(
        Currency,
        { 'iso3': 'ZAR' },
        db_engine,
    )

    with Session(db_engine) as db_session:
        with db_session.begin():         

            seed_client_accounts = [
                IssuingBankClientAccount(
                    currency_id = currency.id,
                    external_id = uuid.uuid4(),
                    name = f'Client {i}',
                    card_pan = random_card_pan_for_bin(bin),
                    card_aid = aid,
                    card_app_label = application_label,
                    date_of_birth = (datetime.datetime.now() - datetime.timedelta(days=365*random.randint(min_age, max_age))).date(),
                    postal_code=''.join(random.sample('0123456789', 6)),
                ) for i,_ in enumerate(range(3))
            ]

            existing_client_accounts = db_session.execute(
                select(IssuingBankClientAccount)
            ).scalars().all()

            for seed_ac in seed_client_accounts:
                if len([existing_ac for existing_ac in existing_client_accounts if existing_ac.name == seed_ac.name]) == 0:
                    db_session.add(seed_ac)
            
            db_session.flush()


def seed_issuing_bank_write_model(db_engine: Engine):
    seed_issuing_bank_client_accounts(db_engine)
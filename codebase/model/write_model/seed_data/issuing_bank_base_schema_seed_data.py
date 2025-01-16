import random
import uuid
from model.write_model.objects.currency import Currency
from model.write_model.objects.emv import random_card_pan_for_bin
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccount
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

def seed_issuing_bank_client_accounts(db_engine: Engine):

    with Session(db_engine) as db_session:
        with db_session.begin():         

            existing_currencies = db_session.execute(
                select(Currency)
            ).scalars().all()

            currency = random.sample(existing_currencies, 1)[0]

            min_age = 18
            max_age = 65
            
            bin = '484795'
            aid = 'A0000000031010'
            application_label = 'Visa Debit'

            seed_client_accounts = [
                IssuingBankClientAccount(
                    currency_id = currency.id,
                    external_client_id = uuid.uuid4(),
                    external_account_id = uuid.uuid4(),
                    name = 'Software Developer',
                    age = random.randint(min_age, max_age),
                    card_pan = random_card_pan_for_bin(bin),
                    card_aid = aid,
                    card_app_label = application_label
                ),
                IssuingBankClientAccount(
                    currency_id = currency.id,
                    external_client_id = uuid.uuid4(),
                    external_account_id = uuid.uuid4(),
                    name = 'Data Scientist',
                    age = random.randint(min_age, max_age),
                    card_pan = random_card_pan_for_bin(bin),
                    card_aid = aid,
                    card_app_label = application_label
                ),
                IssuingBankClientAccount(
                    currency_id = currency.id,
                    external_client_id = uuid.uuid4(),
                    external_account_id = uuid.uuid4(),
                    name = 'FinTech CEO',
                    age = random.randint(min_age, max_age),
                    card_pan = random_card_pan_for_bin(bin),
                    card_aid = aid,
                    card_app_label = application_label
                ),
                IssuingBankClientAccount(
                    currency_id = currency.id,
                    external_client_id = uuid.uuid4(),
                    external_account_id = uuid.uuid4(),
                    name = 'Venture Capitalist',
                    age = random.randint(min_age, max_age),
                    card_pan = random_card_pan_for_bin(bin),
                    card_aid = aid,
                    card_app_label = application_label
                )
            ]

            existing_client_accounts = db_session.execute(
                select(IssuingBankClientAccount)
            ).scalars().all()

            for seed_ac in seed_client_accounts:
                if len([existing_ac for existing_ac in existing_client_accounts if existing_ac.name == seed_ac.name]) == 0:
                    db_session.add(seed_ac)
            
            db_session.flush()


def seed_issuing_bank_base_schema(db_engine: Engine):
    seed_issuing_bank_client_accounts(db_engine)
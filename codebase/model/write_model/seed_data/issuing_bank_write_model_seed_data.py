import random
import uuid
from model.query import select_all_on_filters, select_first_on_filters
from model.write_model.objects.currency import Currency
from model.write_model.objects.emv import random_card_pan_for_bin
from model.write_model.objects.issuing_bank_write_model import IssuingBankClientAccount
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
import datetime
from faker import Faker


def seed_issuing_bank_client_accounts(db_engine: Engine):
    min_age = 18
    max_age = 65

    bin = "484795"
    aid = "A0000000031010"
    application_label = "Visa Debit"

    currency = select_first_on_filters(
        Currency,
        {"iso3": "ZAR"},
        db_engine,
    )

    with Session(db_engine) as db_session:
        with db_session.begin():
            fake = Faker()

            # Count existing client accounts
            existing_account_count = db_session.query(IssuingBankClientAccount).count()

            if existing_account_count < 5:
                # Calculate how many more accounts to seed
                accounts_to_seed = 5 - existing_account_count
                seed_client_accounts = []

                for _ in range(accounts_to_seed):  # Seed only the required number of accounts
                    customer_name = fake.name()
                    seed_account = IssuingBankClientAccount(
                        currency_id=currency.id,
                        external_id=uuid.uuid4(),
                        name=customer_name,
                        card_pan=random_card_pan_for_bin(bin),
                        card_aid=aid,
                        card_app_label=application_label,
                        date_of_birth=(
                            datetime.datetime.now()
                            - datetime.timedelta(days=365 * random.randint(min_age, max_age))
                        ).date(),
                        postal_code="".join(random.sample("0123456789", 6)),
                    )
                    seed_client_accounts.append(seed_account)

                for seed_ac in seed_client_accounts:
                    db_session.add(seed_ac)

                db_session.flush()


def seed_issuing_bank_write_model(db_engine: Engine):
    seed_issuing_bank_client_accounts(db_engine)

import uuid
from model.write_model.objects.platform_write_model import PlatformBank, PlatformBankConfig, PlatformMerchant, PlatformMerchantConfig
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

def seed_platform_merchants(db_engine: Engine):

    with Session(db_engine) as db_session:
        with db_session.begin():         

            seed_merchants = [
                PlatformMerchant(
                    name = 'Vaal Marina Supermarket',
                    callback_url = 'http://merchant_pos_callback:8777',
                    external_id = uuid.uuid4()
                ),
            ]

            seed_merchant_config = PlatformMerchantConfig(
                merchant_address = 'Vaal Marina Supermarket',
                merchant_categorisation_code = '5411',
            )

            existing_merchants = db_session.execute(
                select(PlatformMerchant)
            ).scalars().all()

            for seed_merchant in seed_merchants:
                if len([existing_merchant for existing_merchant in existing_merchants if existing_merchant.name == seed_merchant.name]) == 0:
                    
                    db_session.add(seed_merchant)
                    seed_merchant_config.merchant = seed_merchant
                    db_session.add(seed_merchant_config)
            
            db_session.flush()


def seed_platform_banks(db_engine: Engine):

    with Session(db_engine) as db_session:
        with db_session.begin():         

            seed_banks = [
                PlatformBank(
                    name = 'TB',
                    callback_url = 'http://iss_bank_callback:8777'
                ),
            ]

            seed_bank_config = PlatformBankConfig(
                card_bin = '484795',        
            )

            existing_banks = db_session.execute(
                select(PlatformBank)
            ).scalars().all()

            for seed_bank in seed_banks:
                if len([existing_bank for existing_bank in existing_banks if existing_bank.name == seed_bank.name]) == 0:
                    
                    db_session.add(seed_bank)
                    seed_bank_config.bank = seed_bank
                    db_session.add(seed_bank_config)
            
def seed_platform_write_model(db_engine: Engine):
    seed_platform_merchants(db_engine)
    seed_platform_banks(db_engine)
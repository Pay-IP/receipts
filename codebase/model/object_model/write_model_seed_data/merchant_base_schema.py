from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from model.object_model.write_model.merchant_write_model import SKU

def seed_merchant_base_schema(db_engine: Engine):

    seed_skus = [
        SKU(name="espresso", price=3000),
        SKU(name="filter coffee", price=3500),
        SKU(name="cuppacino", price=4300),
        SKU(name="swiss coffee", price=4800),
    ]

    with Session(db_engine) as db_session:

        with db_session.begin():            

            # SKUs

            existing_skus = db_session.execute(
                select(SKU)
            ).scalars().all()

            for sku in seed_skus:
                if len([sku for sku in existing_skus if sku.name == sku.name]) == 0:
                    db_session.add(sku)
            
            db_session.flush()

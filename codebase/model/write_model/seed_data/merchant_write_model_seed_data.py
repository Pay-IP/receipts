import uuid
from model.write_model.objects.merchant_write_model import SKU, PaymentProcessor
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from util.web import serialize_uuid

# from model.object_model.write_model.merchant_write_model import SKU, PaymentProcessor


def seed_merchant_skus(db_engine: Engine):
    seed_skus = [
        SKU(
            name="Espresso",
            price=3000,
            img="assets/img/espresso.jpeg",
            category="Hot Drinks",
            additional_info="",
        ),
        SKU(
            name="Filter Coffee",
            price=3500,
            img="assets/img/filter.png",
            category="Hot Drinks",
            additional_info="",
        ),
        SKU(
            name="Cuppacino",
            price=4000,
            img="assets/img/cuppachino.jpeg",
            category="Hot Drinks",
            additional_info="",
        ),
        SKU(
            name="Swiss Coffee",
            price=4500,
            img="assets/img/swiss.jpeg",
            category="Hot Drinks",
            additional_info="",
        ),
        SKU(
            name="White Dress",
            price=50000,
            img="assets/img/white_dress.png",
            category="Clothes",
            additional_info="",
        ),
        SKU(
            name="Springbok Jersey",
            price=70000,
            img="assets/img/springbok-jersey.png",
            category="Clothes",
            additional_info="",
        ),
        SKU(
            name="Blue Shirt",
            price=20000,
            img="assets/img/blue_shirt.png",
            category="Clothes",
            additional_info="",
        ),
        SKU(
            name="Slippers",
            price=35000,
            img="assets/img/slippers.png",
            category="Clothes",
            additional_info="",
        ),
        SKU(
            name="Laptop",
            price=1170000,
            img="assets/img/laptop.png",
            category="Electronics",
            additional_info="2 Year Warranty",
        ),
        SKU(
            name="TV",
            price=520000,
            img="assets/img/tv.png",
            category="Electronics",
            additional_info="12 Months Warranty",
        ),
        SKU(
            name="Headphones",
            price=60000,
            img="assets/img/headphone.jpg",
            category="Electronics",
            additional_info="",
        ),
    ]

    with Session(db_engine) as db_session:
        with db_session.begin():
            existing_skus = db_session.execute(select(SKU)).scalars().all()

            for sku in seed_skus:
                if len([sku for sku in existing_skus if sku.name == sku.name]) == 0:
                    db_session.add(sku)

            db_session.flush()


def seed_merchant_payment_processors(db_engine: Engine):
    payment_processors = [
        PaymentProcessor(name="Nedbank", merchant_reference=serialize_uuid(uuid.uuid4())),
    ]

    with Session(db_engine) as db_session:
        with db_session.begin():
            existing_processors = db_session.execute(select(PaymentProcessor)).scalars().all()

            for processor in payment_processors:
                if (
                    len(
                        [
                            processor
                            for processor in existing_processors
                            if processor.name == processor.name
                        ]
                    )
                    == 0
                ):
                    db_session.add(processor)

            db_session.flush()


def seed_merchant_write_model(db_engine: Engine):
    seed_merchant_skus(db_engine)
    seed_merchant_payment_processors(db_engine)

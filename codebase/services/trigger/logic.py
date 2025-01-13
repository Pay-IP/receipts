import random

from model.write_model.objects.common import Currency
from model.write_model.objects.merchant_write_model import SKU
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from services.merchant_pos_new_checkout.client import MerchantPosNewCheckoutClient
from services.merchant_pos_new_checkout.rqrsp import MerchantPosNewCheckoutRequest, MerchantPosNewCheckoutRequestItem
from services.trigger.rqrsp import TriggerRequest
from util.service.service_config_base import ServiceConfig

def random_merchant_pos_new_checkout_request(
    write_model_db_engine: Engine,
    max_count_per_sku = 3,
    sales_tax_percent = 14.0
) -> MerchantPosNewCheckoutRequest:
    
    currencies: list[Currency] = None
    skus: list[SKU] = None

    # Example query
    #user = session.query(User).filter(User.email == "john.doe@example.com").first()

    with Session(write_model_db_engine) as session:

        currencies = session.query(Currency).all()
        skus = session.query(SKU).all()

    lines = []

    for sku in random.sample(skus, random.randint(1, len(skus))):

        sku_count = random.randint(1, max_count_per_sku)

        lines.append(
            MerchantPosNewCheckoutRequestItem(
                sku_id = sku.id,
                sku_count = sku_count,
                # currency_amount = sku.price * sku_count
            )
        )

    currency = random.sample(currencies, 1)[0] 

    return MerchantPosNewCheckoutRequest(
        client_id = None,    
        items = lines,
        currency = currency.iso3,
    )

def handle_trigger_merchant_pos_new_checkout_request(config: ServiceConfig, rq: TriggerRequest):

    merchant_pos_checkout_rq =  random_merchant_pos_new_checkout_request(
        write_model_db_engine=config.write_model_db_engine()
    )

    return MerchantPosNewCheckoutClient().post(merchant_pos_checkout_rq)

from services.merchant_pos_new_checkout.logic import random_merchant_pos_new_checkout_request
from services.merchant_pos_new_checkout.client import MerchantPosNewCheckoutClient
from util.service.service_config_base import ServiceConfig

def handle_trigger_random_merchant_pos_new_checkout_request(
    config: ServiceConfig
):

    return MerchantPosNewCheckoutClient().post(
        random_merchant_pos_new_checkout_request(
            write_model_db_engine=config.write_model_db_engine()
        )
    )

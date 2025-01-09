from services.fetch_buy_orders.logic import configure_get_buy_orders, get_buy_orders_log_event, handle_get_buy_orders
from model.object_model.logevent import HealthChecked
from util.service.service_base import register_healthcheck_endpoint
from util.structured_logging import log_event
from fastapi import FastAPI
from util.service.service_base import request_handler

api = FastAPI()

def configure_api(read_model_engine):
    configure_get_buy_orders(read_model_engine)

register_healthcheck_endpoint(api)

@api.get("/buy_orders")
def get_buy_orders(last_reference: str = None, page_size: int = 10):
    return request_handler(
        'get_btc_buy_price_quote', 
        get_buy_orders_log_event, 
        handle_get_buy_orders
    )(last_reference, page_size)
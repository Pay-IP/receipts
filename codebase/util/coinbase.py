import traceback
from model.object_model.logevent import CoinbaseClientExceptionOccurred
from model.object_model.core.endpoint import Endpoint
from util.structured_logging import log_event
from pydantic import BaseModel
from util.web import http_get, url_for_endpoint
import requests

class CoinbasePriceQuote(BaseModel):
    base: str
    currency: str
    amount: str

class CoinbasePriceQuoteResponse(BaseModel):
    data: CoinbasePriceQuote

class CoinBaseClient:
    
    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    def fetch_btc_price_quote(self, price_type: str, currency: str):

        url = f'{url_for_endpoint(self.endpoint)}/{price_type}'
        try:
            json = http_get(url, json={ 'currency': currency }).json()
            cb_rsp = CoinbasePriceQuoteResponse.parse_obj(json)
            return cb_rsp.data
        except:
            log_event(
                CoinbaseClientExceptionOccurred(
                    currency = currency,
                    price_type = price_type,
                    info = traceback.format_exc()
                )
            )
            raise

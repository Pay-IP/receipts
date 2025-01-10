from model.core.objects.endpoint import Endpoint
from util.web import http_get, url_for_endpoint

from services.btc_price.rqrsp import GetBtcPriceQuoteResponse

class BtcPriceServiceClient:

    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    def get_buy_price(self, currency: str):

        url = f'{url_for_endpoint(self.endpoint)}/buy'
        http_rsp = http_get(url, json={ 'currency': currency }) 
        
        if http_rsp.status_code != 200:
            raise f'get buy price error: {http_rsp.text}'

        return GetBtcPriceQuoteResponse.parse_raw(http_rsp.text).rate
    
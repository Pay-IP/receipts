from enum import Enum
from typing import Optional

MAX_BUY_ORDER_SIZE_EXCLUSIVE_ANY_CURRENCY_UNIT = 1000000000
BUY_ORDER_BOOK_THRESHOLD_BTC = 1000000

BTC_RATE_PRECISION = 40
BTC_RATE_SCALE = 20

class Currency(str, Enum):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    ZAR = 'ZAR'

SUPPORTED_CURRENCIES = [x.value for x in [Currency.USD, Currency.EUR, Currency.GBP, Currency.ZAR]]

class Queue(Enum):
    BuyOrder = 'buy_order'
   
EXCHANGE = ''

QUEUE_NAMES = [(q.value) for q in Queue]

class Service(Enum):
    CREATE_BUY_ORDER = 'create_buy_order'
    FETCH_BUY_ORDERS = 'fetch_buy_orders'
    BTC_PRICE = 'btc_price'
    
    MIGRATION = 'migration'
    READ_MODEL_SYNC = 'read_model_sync'

    MERCHANT_POS_NEW_CHECKOUT = 'merchant_pos_new_checkout'
    MERCHANT_POS_CALLBACK = 'merchant_pos_callback'

    PMT_PROC_NEW_PMT = 'pmt_proc_new_pmt'

    ISS_BANK_NEW_PMT = 'iss_bank_new_pmt'
    ISS_BANK_CALLBACK = 'iss_bank_callback'
    
    PLATFORM_NEW_PMT = 'platform_new_pmt'
    PLATFORM_NEW_RECEIPT = 'platform_new_receipt'
    PLATFORM_MATCHING = 'platform_matching'

    TRIGGER = 'trigger'

from model.common import Queue
from pydantic import BaseModel

class Endpoint(BaseModel):
    protocol: str
    host: str
    port: int
    path: Optional[str] = None
    retry_wait_s: int = 1

class DatabaseEndPoint(Endpoint):
    host: str
    port: int
    database: str
    user: str
    pwd: str

class QueueEndpoint(BaseModel):
    host: str
    port: int
    exchange: str
    queue: Queue
    retry_wait_s: int = 1
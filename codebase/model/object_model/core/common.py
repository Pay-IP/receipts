from enum import Enum

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
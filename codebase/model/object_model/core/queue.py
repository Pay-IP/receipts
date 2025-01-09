from enum import Enum

class Queue(Enum):
    BuyOrder = 'buy_order'

QUEUE_NAMES = [(q.value) for q in Queue]

EXCHANGE = ''
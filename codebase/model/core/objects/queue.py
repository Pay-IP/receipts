from enum import Enum

class EventQueue(Enum):
    BuyOrder = 'buy_order'

EVENT_QUEUE_NAMES = [(q.value) for q in EventQueue]

EXCHANGE = ''
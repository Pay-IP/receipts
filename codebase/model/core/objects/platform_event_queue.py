from enum import Enum

class PlatfortmEventQueue(Enum):
    BuyOrder = 'buy_order'
    NewMatchItemReceived = 'new_match_item_received'
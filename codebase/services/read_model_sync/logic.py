from model.orm.read_model import BuyOrderReadModel
from sqlalchemy.orm import Session
from typing import Optional
from model.common import Queue, QueueEndpoint
from util.db import get_tested_database_engine
from util.env import database_endpoint_from_env, queue_endpoint_from_env
from util.queue import connect_blocking_q_listener
import traceback
from util.service.service_config_base import ServiceConfig
from util.structured_logging import log_event
from model.logevent import BuyOrderReadModelSynced, FailedToSyncBuyOrderReadModel
from model.dto import BuyOrderDTO


def new_sync_buy_order(read_model_engine):   

    def sync_buy_order(model_dict: str, ack):
        try:
            dto = BuyOrderDTO.parse_obj(model_dict)            
            
            read_model: Optional[BuyOrderReadModel] = None

            with Session(read_model_engine) as db_session:
                with db_session.begin():            
                    read_model = BuyOrderReadModel(
                        id = dto.id,
                        created_at = dto.created_at, 
                        external_id = dto.external_id,

                        client_id = dto.client_id,

                        currency_id = dto.currency_id,
                        currency_iso3 = dto.currency_iso3,
                        
                        currency_amount = dto.currency_amount,
                        btc_rate = dto.btc_rate,
                        btc_amount = dto.btc_amount
                    )
                    db_session.add(read_model)            

                    log_event(BuyOrderReadModelSynced(id=dto.id))
                    ack()

        except:
            log_event(
                FailedToSyncBuyOrderReadModel(
                    id=dto.id,
                    info=traceback.format_exc()
                )
            )

    return sync_buy_order

def before_launching_read_model_sync_server(config: ServiceConfig):
    
    read_model_engine = get_tested_database_engine(database_endpoint_from_env('READ_MODEL_DB'))
    buy_order_q_ep: QueueEndpoint = queue_endpoint_from_env('Q', Queue.BuyOrder)

    def connect_event_listeners():
        connect_blocking_q_listener(buy_order_q_ep, new_sync_buy_order(read_model_engine))        

    connect_event_listeners()
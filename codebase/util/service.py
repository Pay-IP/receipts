from fastapi.exceptions import HTTPException
import traceback
import uuid
from model.logevent import RequestFailed, RequestReceivedLogEvent, ResponseReturnedLogEvent
from typing import Callable
from util.service_config_base import ServiceConfig, default_service_config
from util.structured_logging import log_event

_service_config: ServiceConfig = None

def request_handler(TRqModel, callback: Callable):

    global _service_config
    _service_config = default_service_config()

    def handle(*args):
        
        rq = args[0]     

        try:
            log_event(RequestReceivedLogEvent(
                rq_type=TRqModel.__name__,
                rq=str(rq)
            ))

            rsp = callback(_service_config, rq)

            log_event(ResponseReturnedLogEvent(
                rsp_type=rsp.__class__.__name__,
                rsp=str(rsp)
            ))

            return rsp
        except:
            error_reference = uuid.uuid4()
            trace = traceback.format_exc()
            print(trace)
            log_event( 
                RequestFailed(
                    request_type=TRqModel.__name__,
                    request=str(rq),
                    error=trace,
                    reference=str(error_reference)
                )
            )
            raise HTTPException(
                status_code=500, 
                detail=f'reference {error_reference} - {trace}'
            )
    
    return handle
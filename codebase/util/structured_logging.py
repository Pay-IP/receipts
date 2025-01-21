import time
from typing import Optional
from model.core.objects.logevent import LoggingTag
from util.env import env_float, env_int, env_str
import traceback
from fluent import sender
from model.core.objects.service import Service
from pydantic.main import BaseModel
import inflection

SERVICE: Service = None

class ExceptionOccurred(BaseModel):
    _tag = 'exception_occurred'
    msg: str
    stack_trace: Optional[str] = ...

class ConnectedToLogging(BaseModel):
    _tag = 'logging_connected'

class FailedToConnectToLogging(BaseModel):
    _tag = 'failed_to_connect_to_logging'
    host: str
    port: int
    info: str

def log_event(event_model: BaseModel):

    tag = inflection.underscore(type(event_model).__name__)
    #print(f'log_event: {LoggingTag.Root.value} - {SERVICE.value}: {event_model}')

    fsender = sender.FluentSender(
        f'{LoggingTag.Root.value}.{SERVICE.value}', 
        host=env_str('LOGGING_HOST'), 
        port=env_int('LOGGING_PORT')
    )

    try:
        fsender.emit(tag, event_model.dict())
    finally:
        fsender.close()


def log_exception(msg):
    log_event(ExceptionOccurred(msg=msg, stack_trace=traceback.format_exc()))


def configure_structured_logging(
    service_: Service, 
    log_on_successful_connection: bool = False
):
    
    global SERVICE
    SERVICE = service_
    
    retry_s = 10

    while True:

        try:
            retry_s = env_float('LOGGING_RETRY_S')
            
            if log_on_successful_connection:
                log_event(ConnectedToLogging())

            break

        except:
            msg = f'{SERVICE.value} failed to connect to logging'
            print(msg)
            time.sleep(retry_s)

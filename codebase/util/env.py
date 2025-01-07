from model.common import DatabaseEndPoint, Endpoint, QueueEndpoint, Queue, Service
import os

def env_str(key: str):
    return os.environ[key]

def env_int(key: str):
    return int(os.environ[key])

def env_float(key: str):
    return float(env_str(key))

def prefix_str_from_prefix(prefix) -> str:

    prefix_str = None
    
    if isinstance(prefix, Service):
        prefix_str = prefix.value
    else:
        prefix_str = str(prefix)

    return prefix_str.upper()


def database_endpoint_from_env(prefix):
    prefix_str = prefix_str_from_prefix(prefix)
    return DatabaseEndPoint(
        protocol='http',
        host=env_str(f'{prefix_str}_HOST'),
        port=env_int(f'{prefix_str}_PORT'),
        database=env_str(f'{prefix_str}_NAME'),
        user=env_str(f'{prefix_str}_USER'),
        pwd=env_str(f'{prefix_str}_PWD'),
        retry_wait_s=env_int(f'{prefix_str}_RETRY_WAIT_S')
    )

def endpoint_from_env(prefix, no_path: bool = True):

    prefix_str = prefix_str_from_prefix(prefix)

    return Endpoint(
        protocol=env_str(f'{prefix_str}_PROTOCOL'),
        host=env_str(f'{prefix_str}_HOST'),
        port=env_int(f'{prefix_str}_PORT'),
        path=env_str(f'{prefix_str}_PATH') if not no_path else None
    )

def service_endpoint_from_env(service: Service):
    return endpoint_from_env(service.value)

def queue_endpoint_from_env(prefix: str, queue: Queue):
    
    prefix_str = prefix_str_from_prefix(prefix)
    
    return QueueEndpoint(
        host=env_str(f'{prefix_str}_HOST'),
        port=env_int(f'{prefix_str}_PORT'),
        exchange=env_str(f'{prefix_str}_EXCHANGE'),
        queue=queue
    )
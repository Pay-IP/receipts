import datetime
from uuid import UUID
import requests
from model.core.objects.endpoint import Endpoint
from util.env import env_int

def url(protocol:str, host:str, port:str, path:str=None):
    root = f'{protocol}://{host}:{port}'
    return root if not path else f'{root}{path}'

def url_for_endpoint(ep: Endpoint):
    return url(ep.protocol, ep.host, ep.port, ep.path)

def http_get(
    url: str,
    timeout_s: int = env_int('HTTP_GET_RQ_CLIENT_TIMEOUT_S'),
):
    return requests.get(url, timeout=timeout_s)


def http_post(
    url: str,
    json: dict,
    timeout_s: int = env_int('HTTP_POST_RQ_CLIENT_TIMEOUT_S')
):
    return requests.post(url, timeout=timeout_s, json=json)


def serialize_datetime(date: datetime.datetime) -> str:
    return date.isoformat()

def deserialize_datetime(date: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(date)

def serialize_uuid(uuid: UUID) -> str:
    return uuid.hex
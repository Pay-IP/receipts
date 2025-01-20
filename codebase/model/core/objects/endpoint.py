from asyncio import Queue
from dataclasses import dataclass
from typing import Optional

from urllib.parse import urlparse

@dataclass(kw_only=True)
class Endpoint:
    host: str
    port: int
    path: Optional[str] = None
    protocol: str = 'http'
    retry_wait_s: int = 1

@dataclass(kw_only=True)
class DatabaseEndPoint(Endpoint):
    database: str
    user: str
    pwd: str
    # host: str
    # port: int

@dataclass(kw_only=True)
class QueueEndpoint(Endpoint):
    exchange: str
    queue: Queue


def endpoint_from_url(url: str) -> Endpoint:

    # urlparse("scheme://netloc/path;parameters?query#fragment")
    components = urlparse(url)

    return Endpoint(
        protocol = components.scheme,
        host = components.hostname,
        port = components.port,
        path = components.path
    )
    
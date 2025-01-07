import json
from pydantic import BaseModel
from model.common import Endpoint
from util.web import http_post, url_for_endpoint

class ServiceClientBase:
    def __init__(self, endpoint: Endpoint, TRq, TRsp):
        self.endpoint = endpoint
        self.TRq = TRq
        self.TRsp = TRsp

    def post(self, rq: BaseModel):

        http_rsp = http_post(
            url = f'{url_for_endpoint(self.endpoint)}',
            json = json.loads(rq.json())
        )

        if http_rsp.status_code != 200:
            raise Exception(str(http_rsp))

        return self.TRsp.parse_raw(http_rsp.text)

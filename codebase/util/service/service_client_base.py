import json
from pydantic import BaseModel
from model.core.objects.endpoint import Endpoint
from util.format import convert_uuids
from util.web import http_post, url_for_endpoint

class ServiceClientBase:
    def __init__(self, endpoint: Endpoint, TRq, TRsp):
        self.endpoint = endpoint
        self.TRq = TRq
        self.TRsp = TRsp

    def post(self, rq: BaseModel):
        payload = convert_uuids(rq.model_dump())

        http_rsp = http_post(
            url = f'{url_for_endpoint(self.endpoint)}',
            json = payload
        )
        if http_rsp.status_code != 200:
            raise Exception(str(http_rsp))

        return self.TRsp.parse_raw(http_rsp.text)

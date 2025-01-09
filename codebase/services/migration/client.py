from model.object_model.core.endpoint import Endpoint
from model.object_model.core.logevent import WaitedForMigrations, WaitingForMigrations
from util.env import endpoint_from_env
from util.web import http_get, url_for_endpoint
import time
from util.structured_logging import log_event
from util.web import url_for_endpoint

class MigrationServiceClient:


    @classmethod
    def wait_until_ready(cls):
        MigrationServiceClient(
            endpoint_from_env('MIGRATION')
        ).wait_for_migrations()

    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint
        self.endpoint.path = '/healthcheck'

    def is_migrated(self):
        try:      
            url = url_for_endpoint(self.endpoint)
            status_code = http_get(url).status_code
            return status_code == 200
        except:
            return False

    def wait_for_migrations(self, 
        log_while_waiting: bool = False,
        log_on_waited: bool = False
    ):

        while True:
            if self.is_migrated():
                break
            
            if log_while_waiting:
                log_event(WaitingForMigrations())
            
            time.sleep(float(self.endpoint.retry_wait_s))

        if log_on_waited:
            log_event(WaitedForMigrations())
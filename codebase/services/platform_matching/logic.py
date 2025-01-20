import datetime
import schedule
import time

from util.service.service_config_base import ServiceConfig

JOB_PERIOD_S = 1
WAIT_PERIOD_S = 0.1


def get_unmatched_receipts_for_time_window():
    pass

def get_unmatched_payments_for_time_window():
    pass


def match_job():
    print(f'match job running ... {datetime.datetime.now()}')


def before_launching_platform_matching_rest_server(config: ServiceConfig):

    read_model_engine = config.read_model_db_engine()

    schedule.every(JOB_PERIOD_S).seconds.do(match_job)

    while True:
        schedule.run_pending()
        time.sleep(WAIT_PERIOD_S)
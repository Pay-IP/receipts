import time
import traceback
from model.core.objects.endpoint import DatabaseEndPoint
from model.core.objects.logevent import DatabaseAlreadyMigrated, DatabaseMigrated, DatabaseMigrationExceptionOccurred, PendingDatabaseMigrationsDetected
from model.write_model.seed_data.common_write_model_seed_data import seed_common_write_model
from model.write_model.seed_data.issuing_bank_write_model_seed_data import seed_issuing_bank_write_model
from model.write_model.seed_data.merchant_write_model_seed_data import seed_merchant_write_model
from model.write_model.seed_data.payment_processor_write_model_seed_data import seed_payment_processor_write_model
from model.write_model.seed_data.platform_write_model_seed_data import seed_platform_write_model
from util.db import get_test_database_engine
from util.env import database_endpoint_from_env
from util.service.service_config_base import ServiceConfig
from util.structured_logging import log_event
from yoyo import read_migrations, get_backend

def get_database_backend_with_retry(
    ep: DatabaseEndPoint,
    max_retries: int = 7,
    initial_retry_interval_ms: int = 500,
    backoff_factor: int = 2,
):
    
    retry_interval_ms = initial_retry_interval_ms
    
    for i in range(max_retries):
        try:
            return get_backend(f'postgresql://{ep.user}:{ep.pwd}@{ep.host}:{ep.port}/{ep.database}')
        except:
            if i == max_retries - 1:
                raise
            
            retry_interval_ms *= backoff_factor
            # TODO log back off and retry event
            print(f'failed to connect to {ep}, backing off and retrying in {retry_interval_ms / 1000} seconds')
            time.sleep(retry_interval_ms / 1000)

def migrate(
    ep: DatabaseEndPoint, 
    relative_folder_path: str
):
    
    try:
        backend = get_database_backend_with_retry(ep)  
        migrations = read_migrations(relative_folder_path)

        migrations_to_apply = backend.to_apply(migrations)

        if len(migrations_to_apply) == 0:
            log_event(DatabaseAlreadyMigrated(
                database=ep.database
            ))
        elif len(migrations_to_apply) > 0:
            
            log_event(PendingDatabaseMigrationsDetected(
                database=ep.database,
                pending_migrations=[migration.id for migration in migrations_to_apply]
            ))

            backend.apply_migrations(migrations_to_apply)

            log_event(DatabaseMigrated(
                database=ep.database,
                migrations_applied=[migration.id for migration in migrations_to_apply]
            ))

    except:
        trace=traceback.format_exc()
        print(trace)
        log_event(DatabaseMigrationExceptionOccurred(database=ep.database, info=trace))
        raise


def migrate_and_seed_write_model(write_model_db_endpoint):
    
    migrate(write_model_db_endpoint, 'model/write_model/migrations')

    write_model_engine = get_test_database_engine(write_model_db_endpoint)
    seed_common_write_model(write_model_engine)
    seed_platform_write_model(write_model_engine)
    seed_issuing_bank_write_model(write_model_engine)
    seed_payment_processor_write_model(write_model_engine)
    seed_merchant_write_model(write_model_engine)


def migrate_and_seed_read_model(read_model_db_endpoint):
    get_test_database_engine(read_model_db_endpoint)
    migrate(read_model_db_endpoint, 'model/read_model/migrations')

def before_launching_migration_server(service_config: ServiceConfig):

    write_model_db_endpoint = database_endpoint_from_env('WRITE_MODEL_DB')
    migrate_and_seed_write_model(write_model_db_endpoint)

    # read_model_db_endpoint = database_endpoint_from_env('READ_MODEL_DB')
    # migrate_and_seed_read_model(read_model_db_endpoint)
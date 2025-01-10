import traceback
from model.core.objects.endpoint import DatabaseEndPoint
from model.core.objects.logevent import DatabaseAlreadyMigrated, DatabaseMigrated, DatabaseMigrationExceptionOccurred, PendingDatabaseMigrationsDetected
from model.write_model.seed_data.common_base_schema import seed_common_base_schema
from model.write_model.seed_data.merchant_base_schema import seed_merchant_base_schema
from util.db import get_tested_database_engine
from util.env import database_endpoint_from_env
from util.service.service_config_base import ServiceConfig
from util.structured_logging import log_event
from yoyo import read_migrations, get_backend

write_model_db_endpoint = database_endpoint_from_env('WRITE_MODEL_DB')
read_model_db_endpoint = database_endpoint_from_env('READ_MODEL_DB')

def migrate(
    ep: DatabaseEndPoint, 
    relative_folder_path: str
):
    
    try:
        backend = get_backend(f'postgresql://{ep.user}:{ep.pwd}@{ep.host}:{ep.port}/{ep.database}')
        
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

def get_write_model_db_engine():
    return get_tested_database_engine(write_model_db_endpoint)    

def get_read_model_db_engine():
    return get_tested_database_engine(read_model_db_endpoint)

def migrate_and_seed_write_model():
    write_model_engine = get_write_model_db_engine()
    migrate(write_model_db_endpoint, 'model/write_model/migrations')
    
    seed_common_base_schema(write_model_engine)
    seed_merchant_base_schema(write_model_engine)


def migrate_and_seed_read_model():
    read_model_engine = get_read_model_db_engine()
    migrate(read_model_db_endpoint, 'model/read_model/migrations')

def before_launching_migration_server(service_config: ServiceConfig):

    migrate_and_seed_write_model()
    migrate_and_seed_read_model()
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

def select_all(TModel, write_model_db_engine: Engine):
    with Session(write_model_db_engine, expire_on_commit=False) as session:
        return list(session.query(TModel).all())
    

def insert_one(item, db_engine: Engine):
    with Session(db_engine, expire_on_commit=False) as db_session:
        with db_session.begin():            
            db_session.add(item)
            db_session.flush()
            return item
        

def insert_all(items, db_engine: Engine):
    with Session(db_engine, expire_on_commit=False) as db_session:
        with db_session.begin():            
            
            for item in items:            
                db_session.add(item)
            
            db_session.flush()
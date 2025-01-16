from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from sqlalchemy.dialects.postgresql import UUID

def select_all(TModel, engine: Engine):
    with Session(engine, expire_on_commit=False) as session:
        return list(session.query(TModel).all())
    
def select_on_id(TModel, id, engine: Engine):
    with Session(engine, expire_on_commit=False) as session:
        return session.query(TModel).filter(TModel.id == id).first()

def select_all_on_filters(TModel, filters: dict, engine: Engine) -> list:
    with Session(engine, expire_on_commit=False) as session:
        return session.query(TModel).filter_by(**filters).all()

def select_first_on_filters(TModel, filters: dict, engine: Engine) -> list:
    with Session(engine, expire_on_commit=False) as session:
        return session.query(TModel).filter_by(**filters).all()[0]

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

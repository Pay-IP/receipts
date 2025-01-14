from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

def select_all(TModel, engine: Engine):
    with Session(engine, expire_on_commit=False) as session:
        return list(session.query(TModel).all())
    
def select_on_id(engine: Engine, TModel, id):
    with Session(engine, expire_on_commit=False) as session:
        return session.query(TModel).filter(TModel.id == id).first()

def select_on_filters(engine: Engine, TModel, filters: dict) -> list:
    with Session(engine, expire_on_commit=False) as session:
        return session.query(TModel).filter_by(**filters).all()

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
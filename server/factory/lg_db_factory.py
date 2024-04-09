# database_factory.py
from sqlalchemy import create_engine
from langchain.utilities import SQLDatabase
from factory import db, create_app


def create_lg_database():
    app = create_app()

    with app.app_context():
        engine = db.engine
        lg_database = SQLDatabase(engine=engine)
        return lg_database

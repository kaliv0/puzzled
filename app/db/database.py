from os import getenv
from os.path import dirname, join

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_config_path = join(dirname(__file__), "config")
dotenv_path = join(db_config_path, ".env")
load_dotenv(dotenv_path)
SQLALCHEMY_DATABASE_URL = getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

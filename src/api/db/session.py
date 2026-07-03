
import sqlmodel
from sqlmodel import Session
from .config import DATABASE_URL
import time
from sqlalchemy import text

if DATABASE_URL is None or DATABASE_URL == "":
    raise ValueError("DATABASE_URL is not set")

engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    print("Initializing database...")
    max_retries = 5
    retry_delay = 2
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            sqlmodel.SQLModel.metadata.create_all(engine)
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to database after {max_retries} attempts: {e}")
                raise

def get_session():
    with Session(engine) as session:
        yield session


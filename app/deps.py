from sqlmodel import SQLModel, create_engine, Session
from app.config import settings
import os

if not os.path.exists("./data"):
    os.makedirs("./data", exist_ok=True)
engine = create_engine(settings.DB_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)

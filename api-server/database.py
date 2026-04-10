from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///../db/logs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class LogRecord(Base):
    __tablename__ = "logs"

    id        = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String)
    device_id = Column(String, index=True)
    severity  = Column(String, index=True)
    message   = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
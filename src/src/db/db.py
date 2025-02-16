
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from src.utils.common import logger
from src.utils import config

#Postgres
engine = create_engine(url=config.DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base = declarative_base()

#redis
#cache_token  = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
#cache_passwd = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=1, charset="utf-8", decode_responses=True)

#Create all tables
async def init_db() -> None:
  logger.info("initializing the database")
  Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@contextmanager 
def get_db2():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

#Close all DB connections
async def close_db() -> None:
  logger.info("closing all database connections")
  engine.dispose(close=True)


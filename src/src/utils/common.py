from pydantic import BaseModel
from logging.config import dictConfig
from typing import Any, Generic, TypeVar
from fastapi import Query, UploadFile, BackgroundTasks, Request
from passlib.context import CryptContext
from src.utils import config
import logging
import string, random

logger = logging.getLogger("default")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

M = TypeVar("M", bound=BaseModel)

class Response(BaseModel, Generic[M]):   
    status: str
    message: str
    limit:int = 0
    page: int = 0
    count: int = 0
    data: Any = None

class ResponsePlain(BaseModel, Generic[M]):
    status: str
    message: str
    data: Any = None

class LogConfig(BaseModel):

    LOGGER_NAME: str = "default"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },

    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }

dictConfig(LogConfig().model_dump())

def paginate(limit:int=Query(default=50, gt=0), page:int=Query(default=1, gt=0), order_by:str=Query(default="id"), sort_by:str=Query(default="asc", regex="^(asc|desc)$")):
  return {"limit": limit, "page": page, "order_by": order_by, "sort_by": sort_by}

def getFilterParams(request:Request):
    filter_params = {}
    for k, v in request.query_params.items():
        if k not in ["limit", "page", "order_by", "sort_by"]:
            filter_params[k] = v
    return filter_params


class CustomError(Exception):
    def __init__(self, message, details=""):
        super().__init__(message)
        self.details = details

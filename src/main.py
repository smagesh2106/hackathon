from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.utils.common import logger
from src.db.db import init_db, close_db
from src.utils.auth import initialize_db
from src.db import model as model
from datetime import datetime
from src.apps.router import router 
from starlette.middleware.base import BaseHTTPMiddleware
import os
from src.utils import config
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = config.CORS_ALLOW_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                # Specifies allowed origins
    allow_credentials=True,               # Allow cookies and other credentials
    allow_methods=["*"],                  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                  # Allow all headers
)
#lifespan = app.router.lifespan_context

@asynccontextmanager
async def lifespan_wrapper(app: FastAPI):
  await on_startup()
  logger.info( "Application started at {date}".format(date=datetime.now()) )
  yield
  await on_shutdown()
  logger.info( "Application terminated at {date}".format(date=datetime.now()) )

app.router.lifespan_context = lifespan_wrapper

#initialize application
async def on_startup():
  await init_db()
  await initialize_db()

#clean up application
async def on_shutdown():
  await close_db()

#import all routers
app.include_router(router=router, prefix="/api/v1" )



"""
if __name__ == "__main__":
  app = FastAPI()

  app.router.lifespan_context = lifespan_wrapper
 
  app.mount("/uploads", StaticFiles(directory=file_location), name="uploads")
  #middlewares first
  app.add_middleware(BaseHTTPMiddleware,dispatch=audit_log)
  #app.add_middleware(BaseHTTPMiddleware,dispatch=dummy)
  #import all routers
  app.include_router(router=router, prefix="/api/v1" )
  uvicorn.run(app, host="0.0.0.0", port=8000)
"""


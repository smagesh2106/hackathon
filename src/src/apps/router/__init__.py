from fastapi import APIRouter, Depends
from .sensitiveinfo import router as prompt_router

from src.utils import config

router = APIRouter()

router.include_router(router=prompt_router, prefix="/prompt", tags=["Prompt"])

#dashboard.
@router.get("/")
async def index():
  return {"message": f"Hello World : {config.APP_HOST}  - {str(config.APP_PORT)}" }
import time
from fastapi import HTTPException, status, Request, Depends
import jwt
from src.utils import config
from src.utils.common import logger, CustomError
from src.db.db import get_db, get_db2
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from src.db import model as model
from src.apps.schema import sensitiveinfo as schema

import uuid, json

#Initialize Database
async def initialize_db():
    with open("data/db_init.json", "r") as f:
        data = json.load(f)
        #update default permissions
        if data["infos"] is not None:
            with get_db2() as db:       
                for dat in data["infos"]:
                    #id, info = dat["id"], dat["info"]
                    prompt =  dat["info"]
                    #infoSchema = schema.SensitiveInfo(id=int(id), info = info) #if ids are generated
                    infoSchema = schema.SensitiveInfoInput( info = str(prompt))
                    info_db = model.SensitiveInfo(**infoSchema.model_dump())        
                    db.add(info_db)
                    try:
                        db.commit()
                    except Exception as e:
                        db.rollback()
                        logger.warning(f"could not initialize info db, maybe already initialized :{repr(e)}")
                    finally:
                        db.close()


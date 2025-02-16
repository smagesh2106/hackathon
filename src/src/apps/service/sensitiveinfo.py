from sqlalchemy import func, select, asc, desc, and_, or_
from sqlalchemy.orm import Session, joinedload
from src.db import model
import src.apps.schema.sensitiveinfo as schema
from src.utils.common import logger, CustomError

async def getAll(db: Session, limit: int, page: int, order_by: str, sort_by: str, filter_params:dict): 

  filter_oper = "and"
  query = db.query(model.SensitiveInfo)
  filter_value = filter_params.pop("filter_type", "and")

  if (filter_value and (filter_value == "or")):
    filter_oper = "or"

  #filter builder
  filter_list = []
  for k, v in  filter_params.items():
    if( k == "info"):
      filter_list.append(model.SensitiveInfo.info.icontains(f"%{v}%"))
      
  #filter and | or
  if filter_oper == "and":
    query = query.filter(and_(*filter_list))
  else:
    query = query.filter(or_(*filter_list))

  #sort_by and order_by
  if sort_by == "asc": 
    #include pagination
    query = query.order_by(asc(getattr(model.SensitiveInfo, order_by))).limit(limit).offset((page - 1) * limit)
  else:
    #include pagination
    query = query.order_by(desc(getattr(model.SensitiveInfo, order_by))).limit(limit).offset((page - 1) * limit)

  infos = query.all()
  if infos:
    return infos     
  else:
    logger.error("No sensitive infos found")
    return []


async def get_byId(db: Session, id: int):
  dept  = db.query(model.SensitiveInfo).filter(model.SensitiveInfo.id == id).first()
  if dept:
    return dept
  else:
    logger.error(f"No dept found for id: {id}")
    raise CustomError(message=f"dept not found for id: {id}")


async def query_prompt(db: Session, substring: str):
  dept  = db.query(model.SensitiveInfo).filter(model.SensitiveInfo.info.like(f'%{substring}%')).first()
  if dept:
    return True
  else:
    return False


async def create_info(db: Session, prompt: schema.SensitiveInfoInput):
  _db = model.SensitiveInfo(**prompt.model_dump())
  existing_info = db.scalar(select(model.SensitiveInfo).where(model.SensitiveInfo.info == prompt.info))

  if existing_info is not None:
    logger.error(f"dept with name {prompt.info} already exists")
    raise CustomError(message=f"info already exists = {prompt.info}")
  elif _db:  
    db.add(_db)
    try:
      db.commit()
      db.refresh(_db)
      return _db 
    except Exception as e:
      db.rollback()
      logger.error(f"Could not create info, error={repr(e)}")
      raise CustomError(message=f"Could not create info, error={repr(e)}")
  else:
    logger.error(f"Could not create info  = {prompt.info}")
    raise CustomError(message=f"Could not create info  = {prompt.info}")


async def update_info(db:Session, id:int, new_data: schema.SensitiveInfoUpdate):
  dept = db.query(model.SensitiveInfo).filter(model.SensitiveInfo.id == id).first()
  if dept:
    child_data = new_data.model_dump(exclude_unset = True)

    for key, value in child_data.items():
      setattr(dept, key, value)

    db.add(dept)
    try:
      db.commit()
      db.refresh(dept)
      return dept
    except Exception as e:
      db.rollback()
      logger.error(f"Could not update sensitive info id={id}, error={repr(e)}")
      raise CustomError(message=f"Could not update sensitive info id={id}, error={repr(e)}")  
  else:
    logger.error(f"Could not find sensitive info id={id}, error={repr(e)}")
    raise CustomError(message=f"Could not find sensitive info id={id}, error={repr(e)}")  


async def delete_info_byId( db: Session, id: int):
  dept = db.query(model.SensitiveInfo).filter(model.SensitiveInfo.id == id).first()
  if dept:
    db.delete(dept)
    try:
      db.commit()
      return
    except Exception as e:
      logger.error(f"Could not delete sensitive info id={id}, error= {repr(e)}")
      raise CustomError(message=f"Could not delete sensitive info id={id}, error= {repr(e)}")
  else:
    raise CustomError(message=f"sensitive info not found for id: {id}")
from fastapi import Depends, APIRouter, Query, HTTPException, status, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import src.apps.schema.sensitiveinfo as schema
from src.db.db import get_db
from src.apps.service  import sensitiveinfo as service
from src.utils.common import logger, Response, ResponsePlain, paginate, getFilterParams
from src.db import model

router = APIRouter()

async def getRecordCount(db: Session, model: model.SensitiveInfo):
    return db.query(model).count()

#Get all Departments
@router.get("/", response_model=Response, status_code=200)
async def get_all_prompts(page:dict=Depends(paginate), filter_params = Depends(getFilterParams),db: Session = Depends(get_db)):
  try:
    departments = await service.getAll(db, page["limit"], page["page"], page["order_by"], page["sort_by"], filter_params) 
    count  = await getRecordCount(db, model.SensitiveInfo)
    return Response(status="success", message="Sensitive prompts retrieved successfully", data=jsonable_encoder(departments), 
                    count=count, page=page["page"], limit=page["limit"]) 
  except Exception as e:
    logger.error(f"could not list sensitive prompts, error={repr(e)}")    
    raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,detail=f"sensitive prompts not found")

#Get department by ID
@router.get("/{id}", response_model=ResponsePlain, status_code=200)
async def get_prompt_byId(id:int, db: Session = Depends(get_db)):
  try:  
    dept = await service.get_byId(db, id) 
    return ResponsePlain( status="success",  message="sensitive prompt retrieved successfully", data=jsonable_encoder(dept))
  except Exception as e:
    logger.error(f"Could not get sensitive prompt for id  = {id}, error:{repr(e)}")
    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,detail=f"Sensitive prompt with ID={id} does not exist")

#Create Department
@router.post("/", response_model=ResponsePlain, status_code=201)
#async def create_prompt(db: Session = Depends(get_db), prompt: str = Form(...)):  
async def create_prompt(prompt: schema.SensitiveInfoInput, db: Session = Depends(get_db)):  
  try:
    #dept = schema.SensitiveInfoInput(info=prompt)
    #response = await service.create_info(db, dept)
    response = await service.create_info(db, prompt)
    return ResponsePlain(status="success", message="sensitive prompt created successfully", data=jsonable_encoder(response))
  except Exception as e:
    logger.error(f"Could not create sensitive prompt for name  = {prompt.info}, error:{repr(e)})")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not create sensitive prompt = {prompt.info}")
  
#update Department
@router.put("/{id}",  response_model=ResponsePlain, status_code=200 )
async def update_prompt(id:int, prompt: schema.SensitiveInfoInput, db: Session = Depends(get_db)):
  raw_data = {"info":prompt.info}
  user_data = {k:v for k,v in raw_data.items() if v is not None}
  try:
    new_data = schema.SensitiveInfoUpdate(**user_data)
    dept = await service.update_info(db, id, new_data) 
    return ResponsePlain(status="success", message="sensitive prompt updated successfully", data=jsonable_encoder(dept))
  except Exception as e:
    logger.error(f"Could not update sensitive prompt id  = {id}, error:{repr(e)})")
    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,detail=f"Could not update sensitive prompt id  = {id}, error:{repr(e)})")

#delete department
@router.delete("/{id}", response_model=ResponsePlain, status_code=200)
async def delete_prompt( id:int, db: Session = Depends(get_db)):
  try:
    await service.delete_info_byId(db, id)
    return ResponsePlain( status="success",  message="sensitive prompt deleted successfully")
  except Exception as e:
    logger.error(f"Could not delete sensitive prompt id  = {id}, error:{repr(e)})")
    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,detail=f"Could not delete sensitive prompt = {id}, error:{repr(e)})")
  
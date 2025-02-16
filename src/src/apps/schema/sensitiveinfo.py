from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
from datetime import datetime
from typing import Optional, List
from datetime import datetime

#----------Department Schema-------------------
class SensitiveInfoInput( BaseModel):
  info: str  #=  Field(..., min_length=3, max_length=256)

  class Config:
    from_attributes      = True
    str_strip_whitespace = True


class SensitiveInfoUpdate( BaseModel):
  info: str  #=  Field(None, min_length=3, max_length=256)

  class Config:
    from_attributes      = True
    str_strip_whitespace = True


class SensitiveInfo(SensitiveInfoInput):
  id: int# = Field(..., gt=0)
  created_at: datetime|None = None
  updated_at: datetime|None = None
  
  class Config:
    from_attributes = True
    str_strip_whitespace = True

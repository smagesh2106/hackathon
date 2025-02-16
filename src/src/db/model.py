#from __future__ import annotations
from typing import List
from sqlalchemy import Table, ForeignKey, Integer, DateTime, func, String, Boolean, Date
from sqlalchemy import Integer, Column, String, UniqueConstraint
from sqlalchemy.orm import relationship
from src.db.db import Base
from sqlalchemy.inspection import inspect

#+++++++++++++++++++++++++++++++++ Common tables +++++++++++++++++++++++++++++
class TimestampMixin:
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

#+++++++++++++++++++++++++++++++++ Organization +++++++++++++++++++++
class SensitiveInfo(Base, TimestampMixin):
  __tablename__ = "sensitiveinfo"

  id       = Column(Integer, primary_key=True, index=True)
  info     = Column(String, nullable=False, unique=True)

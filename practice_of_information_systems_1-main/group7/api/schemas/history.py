from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class HistoryCreate(BaseModel):
    userId: int
    imageBase64: str
    step: int
    
   
class HistoryResponse(BaseModel):
    id: int
    userId: int
    imageBase64: str #blob
    createdAt: datetime
    class Config:
        orm_mode = True

class HistoryWithParamResponse(BaseModel):
    id: int
    userId: int
    imageBase64: str #blob
    stapleValue: int
    sideValue: int
    mainValue: int
    otherValue: int
    createdAt: datetime
    class Config:
        orm_mode = True
from typing import Optional

from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    userName: str
    age: int
    sex: int
    height: float
    weight: float

class UserCreateResponse(BaseModel):
    id: int
    userName: str = Field("NoName", example="Taro")
    status: int
    stapleValue: int
    mainValue: int
    sideValue: int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    userName: str = Field(None, example="Taro")
    status: int
    stapleValue: int
    mainValue: int
    sideValue: int

    class Config:
        orm_mode = True
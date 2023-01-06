from urllib import response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.user as user_schema
import api.cruds.user as user_crud
from api.db import get_db
from typing import List, Tuple
import datetime

router = APIRouter()

@router.post("/user-create", response_model=user_schema.UserCreateResponse)
async def user_create(user_create_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    if await user_crud.get_user_by_user_name(db, user_create_body.userName) is None:
        return await user_crud.create_user(db, user_create_body)
    else:
        raise HTTPException(status_code=401, detail="exist user name")


# @router.get("/user/{userId}", response_model=user_schema.UserResponse)
# async def get_user(userId: int, db: AsyncSession = Depends(get_db)):
#     user_info = await user_crud.get_user_by_id(db, id=userId)
#     if user_info is not None:
#         return user_info
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

@router.get("/user-all", response_model = List[user_schema.UserResponse])
async def get_all_user(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_user(db)

@router.get("/user/{userId}", response_model=user_schema.UserResponse)
async def get_user(userId: int, db: AsyncSession = Depends(get_db)):
    user_info = await user_crud.get_user_by_id(db, id=userId)
    if user_info is not None:
        tz = datetime.timezone(datetime.timedelta(hours=9), 'Asia/Tokyo')
        now = datetime.datetime.now(tz)
        updatedAt_tz = user_info.updatedAt
        print("今何時",now)
        print("updatedAt_tz",updatedAt_tz)
        updatedAt_tz = updatedAt_tz.replace(tzinfo=tz)
        if (now - updatedAt_tz).seconds >= 300:
            return await user_crud.change_state_by_hungry(db, id=userId)
        else:
            return user_info
    else:
        raise HTTPException(status_code=404, detail="User not found")
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model
import api.schemas.user as user_schema

from sqlalchemy.engine import Result
from sqlalchemy import select
from typing import List, Tuple, Optional

async def create_user(
    db: AsyncSession, user_create: user_schema.UserCreate
) -> user_model.User: 
    user = user_model.User(**user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_id(db: AsyncSession, id: int) -> Tuple[int, str, int]:
    result: Result = await (
        db.execute(
            select(
                user_model.User.id,
                user_model.User.userName,
                user_model.User.status,
                user_model.User.stapleValue,
                user_model.User.mainValue,
                user_model.User.sideValue,
                user_model.User.updatedAt
            ).filter(user_model.User.id == id)
        )
    )
    return result.first()

async def get_user_by_id_all_info(db: AsyncSession, id: int) -> Optional[user_model.User]:
    result: Result = await (
        db.execute(
            select(
                user_model.User
            ).filter(user_model.User.id == id)
        )
    )
    user_info: Optional[Tuple[user_model.User]] = result.first()
    return user_info[0] if user_info is not None else None

async def get_user_by_id_for_update_history(db: AsyncSession, id: int) -> Tuple[int, str, int]:
    result: Result = await (
        db.execute(
            select(
                user_model.User.id,
                user_model.User.userName,
                user_model.User.status,
                user_model.User.stapleValue,
                user_model.User.mainValue,
                user_model.User.sideValue  
            ).filter(user_model.User.id == id)
        )
    )
    return result.first()

async def get_user_by_user_name(db: AsyncSession, userName: str) -> Tuple[int, str, int]:
    result: Result = await (
        db.execute(
            select(
                user_model.User.id,
                user_model.User.userName,
                user_model.User.status,
                user_model.User.stapleValue,
                user_model.User.mainValue,
                user_model.User.sideValue
            ).filter(user_model.User.userName == userName)
        )
    )
    return result.first()

async def get_all_user(db: AsyncSession) -> List[Tuple[int, str]]:
    result: Result = await (
        db.execute(
            select(
                user_model.User.id,
                user_model.User.userName,
                user_model.User.status,
                user_model.User.stapleValue,
                user_model.User.mainValue,
                user_model.User.sideValue
            )
        )
    )
    users = result.all()
    return users

async def update_user(db: AsyncSession, status: int, status_stapleValue: int, status_sideValue: int, status_mainValue: int, userId: int) -> user_model.User:
    user_obj = await get_user_by_id_all_info(db, id=userId)
    print("ここは",status_stapleValue, status_sideValue, status_mainValue)
    if user_obj is not None:
        user_obj.status = status 
        user_obj.stapleValue = status_stapleValue
        user_obj.sideValue = status_sideValue
        user_obj.mainValue = status_mainValue
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
    return user_obj


async def change_state_by_hungry(db: AsyncSession, id: int) -> Tuple[user_model.User]:
    result: Result = await(
        db.execute(
            select(
                user_model.User
            ).filter(user_model.User.id == id)
        )
    )
    user: Optional[Tuple[user_model.User]] = result.first()
    user_original = user[0] if user is not None else None
    if user_original is not None:
        user_original.status = 1
        db.add(user_original)
        await db.commit()
        await db.refresh(user_original)
    return user_original


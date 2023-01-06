from sqlalchemy.ext.asyncio import AsyncSession

import api.models.history as history_model
import api.schemas.history as history_schema

from sqlalchemy.engine import Result
from sqlalchemy import select
from typing import List, Tuple

import datetime

async def create_history(
    db: AsyncSession, history_create: history_schema.HistoryCreate, stapleValue: int, sideValue: int, mainValue: int, otherValue: int 
) -> history_model.History:
    # モデルの結果もDBに保存する
    history = history_model.History(**history_create.dict())
    history.imageBase64 = history_create.imageBase64.encode()
    history.stapleValue = stapleValue
    history.sideValue = sideValue
    history.mainValue = mainValue
    history.otherValue = otherValue
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history

async def get_history_by_id(db: AsyncSession, id: int) -> List[Tuple[int, int, str, int, str]]:
    result: Result = await (
        db.execute(
            select(
                history_model.History.id,
                history_model.History.userId,
                history_model.History.imageBase64,
                history_model.History.step,
                history_model.History.createdAt
            ).filter(history_model.History.userId == id)
        )
    )
    return result.all()

async def get_history_by_id_and_last_24_hours(db: AsyncSession, id: int) -> List[Tuple[int, int, str, int, int, int, int, int, str]]:
    tz = datetime.timezone(datetime.timedelta(hours=9), 'Asia/Tokyo')
    day_before = datetime.timedelta(hours=24)
    now = datetime.datetime.now(tz)
    print("1日前",now-day_before)
    print("現在",now)
    result: Result = await (
        db.execute(
            select(
                history_model.History.id,
                history_model.History.userId,
                history_model.History.imageBase64,
                history_model.History.step,
                history_model.History.stapleValue,
                history_model.History.sideValue,
                history_model.History.mainValue,
                history_model.History.otherValue,
                history_model.History.createdAt
            ).filter(history_model.History.userId == id)
            .filter(history_model.History.createdAt >= now-day_before)
            .filter(history_model.History.createdAt <= now)
        )
    )
    return result.all()
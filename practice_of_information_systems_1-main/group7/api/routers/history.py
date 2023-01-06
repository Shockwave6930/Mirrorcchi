from urllib import response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.history as history_schema
import api.cruds.history as history_crud
import api.cruds.user as user_crud
import api.schemas.user as user_schema
import api.utils.health_logic as health_logic
from api.db import get_db
from typing import List, Tuple
import torch
import torchvision
import cv2
import numpy as np
import io
from PIL import Image
import os
import base64

router = APIRouter()

@router.post("/image", response_model=user_schema.UserResponse)
async def history_create(history_create_body: history_schema.HistoryCreate, db: AsyncSession = Depends(get_db)):
    # モデルに画像を読み込ませて結果をまつ
    ## todo: Model Calling?
    # model = torch.load('/src/api/routers/best.pt')
    model = torch.hub.load('/src/api/yolov5', 'custom', path='/src/api/routers/best.pt', source='local')
    img_data = base64.b64decode(history_create_body.imageBase64)
    img_np = np.fromstring(img_data, np.uint8)
    src = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)
    
    # img_pil = Image.open(history_create_body.imageBase64)
    # img_numpy = np.asarray(img_pil)
    # img_numpy_bgr = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR)
    # imgs = [img_numpy_bgr]
    results = model(src)
    print("modelの結果", results)
    results.print()
    print("modelの結果2", results.pandas().xyxy[0].name)
    eatList = results.pandas().xyxy[0].name.tolist()
    print("eatList", eatList)

    stapleValue = 0
    sideValue = 0
    mainValue = 0
    otherValue = 0
    for eat in eatList:
        value = eat.split('-')[1]
        print("valueとは", value)
        if value == "0" or value == "1":
            stapleValue += 1
        elif value == "2":
            sideValue += 1
        elif value == "3" or value == "4":
            mainValue += 1
        elif value == "5":
            otherValue += 1


    # 送られてきた画像情報とモデルの結果をdbに保存する
    history_info = await history_crud.create_history(db, history_create_body, stapleValue, sideValue, mainValue, otherValue)

    # db保存がうまくいった時
    if history_info is not None:
        history_info_24 = await history_crud.get_history_by_id_and_last_24_hours(db, id=history_info.userId)
        print("history_info_24", history_info_24)
        status, status_stapleValue, status_sideValue, status_mainValue = health_logic.decide_status(history_info.step, history_info_24)
        
        update_user = await user_crud.update_user(db, status, status_stapleValue, status_sideValue, status_mainValue, history_info.userId)
        return update_user
        # user_info = await user_crud.get_user_by_id_all_info(db, id=history_info.userId)
        # if user_info is not None:
        #     update_user = await user_crud.update_user(db, status, original=user_info)
        #     return update_user
        # else:
        #     raise HTTPException(status_code=404, detail="User not found")
    # db保存がうまくいかなかったとき
    else:
        raise HTTPException(status_code=500, detail="internal server error")

@router.get("/get-history/{user_id}", response_model = List[history_schema.HistoryResponse])
async def get_history(user_id: int, db: AsyncSession = Depends(get_db)):
    return await history_crud.get_history_by_id(db, id=user_id)

@router.get("/get-history-with-param/{user_id}", response_model = List[history_schema.HistoryWithParamResponse])
async def get_history_with_param(user_id: int, db: AsyncSession = Depends(get_db)):
    return await history_crud.get_history_by_id_and_last_24_hours(db, id=user_id)


from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    userName = Column(String(1024))
    age = Column(Integer, default=0)
    # 1: 男性
    # 2: 女性
    # 3: その他
    sex = Column(Integer, default=3)
    height = Column(Integer, default=0)
    weight = Column(Integer, default=0)
    # 1: お墓
    # 2: やせほそってる
    # 3: 健康
    # 4: ふとってる
    # 5: かなりふとってる
    status = Column(Integer, default=3)
    stapleValue = Column(Integer, default=0)
    sideValue = Column(Integer, default=0)
    mainValue = Column(Integer, default=0)
    otherValue = Column(Integer, default=0)
    updatedAt = Column(
        'updatedAt',
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        onupdate=current_timestamp(),
        comment='最終更新日時',
    )


    

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, BLOB, TEXT, LargeBinary
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from api.db import Base


class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    imageBase64 = Column(MEDIUMTEXT)
    step = Column(Integer)
    stapleValue = Column(Integer, default=0)
    sideValue = Column(Integer, default=0)
    mainValue = Column(Integer, default=0)
    otherValue = Column(Integer, default=0)
    createdAt = Column(
        'createdAt',
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment='登録日時',
    )

    

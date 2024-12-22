from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, Integer, Boolean, sql
from models.db_gino import TimedBaseModel


class TeamSchema(TimedBaseModel):
    __tablename__ = 'teams'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    invite_link = Column(String, unique=True)
    owner_id = Column(BigInteger)
    members_id = Column(String)  # Храним список участников в формате JSON-строки
    members_count = Column(Integer, default=0)
    current_members = Column(Integer, default=1)
    query: sql.Select
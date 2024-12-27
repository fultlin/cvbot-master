from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, Integer, Boolean, sql
from models.db_gino import TimedBaseModel


class UserSchema(TimedBaseModel):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    language = Column(String, default='ru')
    user_id = Column(BigInteger, unique=True)
    role = Column(String, default='user')
    sysadmin = Column(Boolean, default=False)
    state = Column(String, default='main_menu')
    last_online = Column(DateTime, default=datetime.now())
    notification = Column(Integer, default=0)
    bot_blocked = Column(Boolean, default=False)
    username = Column(String)
    name = Column(String)
    timezone = Column(BigInteger, default=0)
    email = Column(String)
    referals_count = Column(Integer, default=0)
    active_referals = Column(Integer, default=0)
    parent = Column(Integer, default=0)
    query: sql.Select

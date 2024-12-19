from sqlalchemy import Column, BigInteger, String, Boolean, sql
from models.db_gino import TimedBaseModel


class SettingSchema(TimedBaseModel):
    __tablename__ = 'settings'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String, unique=True)
    value = Column(String)

    query: sql.Select
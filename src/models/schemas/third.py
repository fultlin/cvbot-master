from sqlalchemy import Column, BigInteger, Float, String, Boolean, DateTime, sql
from models.db_gino import TimedBaseModel


class ThirdSchema(TimedBaseModel):
    __tablename__ = 'third'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    state = Column(String, default='0')
    username = Column(String, default='Не указано')
    query: sql.Select
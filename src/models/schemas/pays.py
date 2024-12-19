from sqlalchemy import Column, BigInteger, Float, String, Boolean, DateTime, sql
from models.db_gino import TimedBaseModel


class PaySchema(TimedBaseModel):
    __tablename__ = 'pays'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    amount = Column(Float)
    plan = Column(String)
    status = Column(String, default='disabled')
    remaining = Column(Float, default=0)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    username = Column(String)
    external = Column(Boolean, default=False)
    name = Column(String)
    query: sql.Select

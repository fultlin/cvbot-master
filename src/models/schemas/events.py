from sqlalchemy import Column, DateTime, BigInteger, String, Boolean, sql
from models.db_gino import TimedBaseModel


class EventsSchema(TimedBaseModel):
    __tablename__ = 'events'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String)
    username = Column(String)
    display_name = Column(String)
    value = Column(String)
    callback = Column(String)
    timestamp = Column(DateTime, nullable=True)

    query: sql.Select

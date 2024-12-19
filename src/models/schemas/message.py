from sqlalchemy import Column, BigInteger, String, Boolean, sql
from models.db_gino import TimedBaseModel


class MessageSchema(TimedBaseModel):
    __tablename__ = 'messages'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(String, unique=True)
    text = Column(String)
    entity = Column(String, nullable=True)
    lang = Column(String, nullable=True)

    query: sql.Select
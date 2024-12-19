from sqlalchemy import Column, BigInteger, String, Boolean, sql
from models.db_gino import TimedBaseModel


class PromosSchema(TimedBaseModel):
    __tablename__ = 'promos'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    value = Column(String)

    query: sql.Select

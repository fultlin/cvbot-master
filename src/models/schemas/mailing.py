from sqlalchemy import Column, BigInteger, String, Boolean, sql
from models.db_gino import TimedBaseModel


class MailingSchema(TimedBaseModel):
    __tablename__ = 'mailings'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=False)
    message_id = Column(BigInteger, unique=True)
    text = Column(String)

    query: sql.Select

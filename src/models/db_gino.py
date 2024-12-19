import logging

import sqlalchemy as sa
from typing import List
from gino import Gino
from sqlalchemy import Column, DateTime

db = Gino()

logger = logging.getLogger(__name__)


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())


async def connect_to_db(remove_data: bool = False):
    import config

    print("Connecting to PostgreSQL...")

    logger.info("Connecting to PostgreSQL...")
    postgres_uri = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/{config.DB_NAME}?statement_cache_size=0?max_inactive_connection_lifetime=3"

    await db.set_bind(postgres_uri)

    if remove_data:
        await db.gino.drop_all()

    await db.gino.create_all()

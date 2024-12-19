from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from datetime import datetime
from models.quick_commands import DbUser, DbPay

class UpdateOnlineMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        result = await handler(event, data)
        user_id = event.from_user.id
        username = event.from_user.username
        name = event.from_user.full_name
        user = DbUser(user_id=user_id)
        await user.update_record(last_online=datetime.now(), username=username, name=name)
        tr = DbPay(user_id=user_id)
        await tr.update_record(username=username, name=name)
        return result

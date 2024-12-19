from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from datetime import datetime
from models.quick_commands import DbUser

class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        result = await handler(event, data)

        user_id = event.from_user.id
        username = event.from_user.username
        user = DbUser(user_id=user_id)

        data['language'] = user.language if user else 'ru'

        return result

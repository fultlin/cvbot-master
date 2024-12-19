from aiogram.filters import Filter
from aiogram.types import Message
from models.quick_commands import DbUser

class StateIs(Filter):
    def __init__(self, state: str):
        self.state = state

    async def __call__(self, message: Message) -> bool:
        user = DbUser(user_id=message.from_user.id)
        state = await user.get_state()

        return state.startswith(self.state) if state else False
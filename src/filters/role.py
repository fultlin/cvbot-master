from aiogram.filters import Filter
from aiogram.types import Message
from models.quick_commands import DbUser

class RoleIs(Filter):
    def __init__(self, role: list[str]):
        self.role = role

    async def __call__(self, message: Message) -> bool:
        user = DbUser(user_id=message.from_user.id)
      #  print(message.from_user.id)
        schema = await user.get_schema()
        data = await schema.query.where(schema.role.in_(self.role)).gino.all()
     #   print(schema)
        users_id = [user.user_id for user in data]
     #   print(users_id)
        return message.from_user.id in users_id
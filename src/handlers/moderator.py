from filters.role import RoleIs

from aiogram import Bot, Router
from aiogram.types import Message

from middlewares.google_sheet import SheetMiddleware
from models.quick_commands import DbUser

moderator = Router()
moderator.message.filter(RoleIs(['moder', 'admin']))

moderator.message.middleware(SheetMiddleware())
moderator.callback_query.middleware(SheetMiddleware())

@moderator.message(lambda message: message.reply_to_message is not None)
async def answer_question(message: Message, bot: Bot) -> None:
    msg_text = message.reply_to_message.text if message.reply_to_message.text else message.reply_to_message.caption
    try:
        full_name = msg_text.split('\n')[1].strip()
        reply_text = msg_text.split('\n\n')[1].strip()
        user_id = int(msg_text.split('\n')[0].strip())
    except:
        print('err')

    # if not message.reply_to_message.forward_from:
    #     return

    # user_id = message.reply_to_message.forward_from.id
    user = DbUser(user_id=user_id)

    if not user:
        if not message.reply_to_message.forward_from.id:
            await message.answer('Закрытый профиль')
            return
        
        await message.answer('Пользователь не найден')

        return

    await bot.send_message(
        chat_id=user_id,
        text=message.text,
    )
    await message.answer('Ответ отправлен пользователю')

    schema = DbUser()
    schema = await schema.get_schema()

    moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

    if moders:
        for u in moders:
            if u.user_id != message.from_user.id:
                await bot.send_message(
                    chat_id=u.user_id,
                    text=f'Модератор {message.from_user.full_name} ответил на вопрос пользователя {full_name}\n\n- {reply_text}\n- {message.text}'
                )

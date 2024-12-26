import json

from aiogram.client.session import aiohttp
from filters.role import RoleIs
from filters.state import StateIs
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

import os

from aiogram.filters import Command, CommandObject

from middlewares.google_sheet import SheetMiddleware
from models.quick_commands import DbUser, DbMessage, DbSetting, DbPay, DbRecent, FirstRecent, SecondRecent, ThirdRecent
from models.schemas.mailing import MailingSchema
from datetime import datetime
from dateutil.relativedelta import relativedelta

from models.schemas.promos import PromosSchema
from models.schemas.events import EventsSchema

from .default import get_message
from models.schemas.settings import SettingSchema

from keyboards.main import get_manage_user_kb, get_back_kb
from keyboards.boss import get_etap_out, get_reach_out, set_reach_pout, ease_link_kb, boss_mark

admin = Router()
admin.message.filter(RoleIs(['admin']))

admin.message.middleware(SheetMiddleware())
admin.callback_query.middleware(SheetMiddleware())

keys = [
    "start",
    "private_community",
    "pay",
    "select_plan",
    "payed",
    "contact",
    "promo_code_not",
    "about_club",
    "education",
    "follow_up_15m",
    "follow_up_1h",
    "follow_up_2h",
    "follow_up_1d",
    "follow_up_2d",
    "follow_up_3d",
    "follow_up_4d",
]


@admin.message(Command('admin'))
async def povelitel(message: Message, bot: Bot) -> None:
    await bot.send_message(message.from_user.id, 'Добро пожаловать криптогений', reply_markup=ease_link_kb())

@admin.callback_query(F.data == 'admin')
async def povelitel(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    await bot.send_message(callback.from_user.id, 'Добро пожаловать криптогений', reply_markup=ease_link_kb())
    
    
@admin.callback_query(F.data == 'reach_out')
async def reachout(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Выберите таблицу', reply_markup=get_reach_out('0'))
    



@admin.callback_query(F.data[:4] == 'rec_')
async def eeetap(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    u_db = DbRecent()
    f_db = FirstRecent()
    s_db = SecondRecent()
    t_db = ThirdRecent()
    data = callback.data  
    
    if data[4] == '0':
        users = await u_db.get_shema()
        await bot.send_message(callback.from_user.id, f'Выберите кого заричаучить😈😈😈😈😈\nСтраница {int(data[8]) + 1}', reply_markup=boss_mark(data[4], data[6], data[8], users))
    elif data[4] == '1':
        users = await f_db.get_shema()
        await bot.send_message(callback.from_user.id, f'Выберите кого заричаучить😈😈😈😈😈\nСтраница {int(data[8]) + 1}', reply_markup=boss_mark(data[4], data[6], data[8], users))
    elif data[4] == '2':
        users = await s_db.get_shema()
        await bot.send_message(callback.from_user.id, f'Выберите кого заричаучить😈😈😈😈😈\nСтраница {int(data[8]) + 1}', reply_markup=boss_mark(data[4], data[6], data[8], users))
    elif data[4] == '3':
        users = await t_db.get_shema()
        await bot.send_message(callback.from_user.id, f'Выберите кого заричаучить😈😈😈😈😈\nСтраница {int(data[8]) + 1}', reply_markup=boss_mark(data[4], data[6], data[8], users))
    elif data[4] == '4':
        users = await u_db.get_shema() + await t_db.get_shema() + await s_db.get_shema() + await f_db.get_shema()
        await bot.send_message(callback.from_user.id, f'Выберите кого заричаучить😈😈😈😈😈\nСтраница {int(data[8]) + 1}', reply_markup=boss_mark(data[4], data[6], data[8], users))

@admin.callback_query(F.data[:3] == 'ri_')
async def change_etap(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id, '')
    data = callback.data
    data = data.split('_')
    q = ''
    if data[2] == '0':
        tab = 'recent'
        q = await DbRecent(user_id=int(data[1])).select_recent()
        print(q)
    elif data[2] == '1':
        tab = 'first'
        q = await FirstRecent(user_id=int(data[1])).select_recent()
    elif data[2] == '2':
        tab = 'second'
        q = await SecondRecent(user_id=int(data[1])).select_recent()
    elif data[2] == '3':
        tab = 'third'
        q = await ThirdRecent(user_id=int(data[1])).select_recent()
    elif data[2] == '4':
        if await DbRecent(user_id=int(data[1])).select_recent():
            q = await DbRecent(user_id=int(data[1])).select_recent()
        elif await FirstRecent(user_id=int(data[1])).select_recent():
            q = await FirstRecent(user_id=int(data[1])).select_recent()
        elif await SecondRecent(user_id=int(data[1])).select_recent():
            q = await SecondRecent(user_id=int(data[1])).select_recent()
        elif await ThirdRecent(user_id=int(data[1])).select_recent():
            q = await ThirdRecent(user_id=int(data[1])).select_recent()
    e = await DbPay(user_id=int(data[1]), status='ended').select_pay()
    await bot.send_message(callback.from_user.id, text=f'User id {data[1]}\n\nUsername {q.username}\nБыл в клубе {e.plan}\n Категория {q.state}', reply_markup=set_reach_pout(q.user_id, q.username, data[2]))
        

@admin.callback_query(F.data[:4] == 'dda_')
async def call_data_process(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id, '')
    data = callback.data
    data = data.split('_')
    tab = 'ХЗ'
    print(data[2], data[3])
    if data[1] == '0':
        data[1] = '1_First reachout'
    if data[1] == '1':
        data[1] = '2_2nd reachout'
    if data[1] == '2':
        data[1] = '3_3rd reachout'
    if data[1] == '3':
        data[1] = '4_Вернётся позже'
    if data[1] == '6':
        user = DbUser(user_id=callback.from_user.id)
        await user.set_state(f'custom_{data[3]}_{data[2]}')
        await bot.send_message(callback.from_user.id, f'Напишите категорию')
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
    else:
        if data[1] == '4':
            data[1] = '9_Вернулся'
            if data[3] == '0':
                q = DbRecent(user_id=int(data[2]))
                tab = 'recent'
                await q.remove()

            elif data[3] == '1':
                tab = 'first'
                q = FirstRecent(user_id=int(data[2]))
                await q.remove()
            elif data[3] == '2':
                tab = 'second'
                q = SecondRecent(user_id=int(data[2]))
                await q.remove()
            elif data[3] == '3':
                tab = 'third'
                q = ThirdRecent(user_id=int(data[2]))
                await q.remove()
        elif data[1] == '5':
            data[1] = '8_Полный отказ'
        if data[3] == '0':
            q = DbRecent(user_id=int(data[2]))
            tab = 'recent'
        # print(q.state)
            await q.update_record(state=data[1])
            print(q.state)
        elif data[3] == '1':
            tab = 'first'
            q = FirstRecent(user_id=int(data[2]))
            await q.update_record(state=data[1])
        elif data[3] == '2':
            tab = 'second'
            q = SecondRecent(user_id=int(data[2]))
            await q.update_record(state=data[1])
        elif data[3] == '3':
            tab = 'third'
            q = ThirdRecent(user_id=int(data[2]))
            await q.update_record(state=data[1])
    
    # await bot.send_message(callback.from_user.id, text=f'User id {data[2]}\n\nUsername {q.username}\nTable {tab}\n Этап {q.state}', reply_markup=set_reach_pout(q.user_id, q.username, data[3]))
        await bot.send_message(callback.from_user.id, text=f'Успешно!')
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        


@admin.message(StateIs('custom_'))
async def set_custom_cat(message: Message):
    user = DbUser(user_id=message.from_user.id)
    data = await user.get_state()
    data = data.replace('custom_', '').split('_')
    ans = '7_' + message.text
    if data[0] == '0':
        q = DbRecent(user_id=int(data[1]))
        tab = 'recent'
        # print(q.state)
        await q.update_record(state=ans)
        print(q.state)
    elif data[0] == '1':
        tab = 'first'
        q = FirstRecent(user_id=int(data[1]))
        await q.update_record(state=ans)
    elif data[0] == '2':
        tab = 'second'
        q = SecondRecent(user_id=int(data[1]))
        await q.update_record(state=ans)
    elif data[0] == '3':
        tab = 'third'
        q = ThirdRecent(user_id=int(data[1]))
        await q.update_record(state=ans)
    await user.set_state('')
    # await bot.send_message(callback.from_user.id, text=f'User id {data[2]}\n\nUsername {q.username}\nTable {tab}\n Этап {q.state}', reply_markup=set_reach_pout(q.user_id, q.username, data[3]))
    await message.reply('Успешно!')
  
 
    
    

@admin.callback_query(F.data =='edit_text')
async def editText(callback: CallbackQuery, bot: Bot) -> None:
    user_id = callback.from_user.id
    user = DbUser(user_id=user_id)

    if not user:
        return

    # Extract the key from the command

    keys_display = "\n".join([f"<code>{key}</code>" for key in keys])

    await bot.send_message(
        chat_id=user_id,
        text=f'Укажите ключ сообщения для редактирования: <code>ключ</code> \n\nДоступные ключи:\n{keys_display}',
        parse_mode='HTML'
    )
    await user.set_state('gdum')

@admin.callback_query(F.data == 'edit_photo')
async def editPhoto(callback: CallbackQuery, bot: Bot) -> None:
    user_id = callback.from_user.id
    user = DbUser(user_id=user_id)

    if not user:
        return

    # Отображаем список доступных ключей
    keys_display = "\n".join([f"<code>{key}</code>" for key in keys])

    await bot.send_message(
        chat_id=user_id,
        text=f'Укажите ключ сообщения для редактирования изображения: <code>ключ</code> \n\nДоступные ключи:\n{keys_display}',
        parse_mode='HTML'
    )
    await user.set_state('edit_photo_key')


@admin.message(StateIs('edit_photo_key'))
async def setPhotoKey(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    user = DbUser(user_id=user_id)
    key = message.text.strip()
    
    msg = DbMessage(key=key)
    db_message = await msg.select_message()

    if not db_message:
        await message.reply(f"Сообщение с ключом '{key}' не найдено.")
        await user.set_state('')
        return

    await user.set_state(f'edit_photo_{key}')
    await message.reply(f"Прикрепите новое изображение для ключа <code>{key}</code>.", parse_mode='HTML')


# @admin.message(StateIs(f'edit_photo_'), lambda message: message.photo is not None)
# async def update_photo(message: Message, bot: Bot) -> None:
#     user_id = message.from_user.id
#     user = DbUser(user_id=user_id)

#     state = await user.get_state()
#     key = state.replace('edit_photo_', '')

#     msg = DbMessage(key=key)
#     db_message = await msg.select_message()

#     if not db_message:
#         await message.reply(f"Сообщение с ключом '{key}' не найдено.", parse_mode='HTML')
#         await user.set_state('')
#         return

#     photo = message.photo[-1]
#     file_path = f"media/{key}.png"
#     await photo.download(destination=file_path)

#     # Удаляем старое изображение (если существует)
#     if db_message.image_path:
#         try:
#             os.remove(db_message.image_path)
#         except FileNotFoundError:
#             pass

#     # Обновляем путь к изображению в базе данных
#     await msg.update_record(image_path=file_path)
#     await message.answer(f"Фото успешно обновлено и сохранено как {file_path}", parse_mode='HTML')

@admin.message(StateIs('gdum'))
async def checkkl(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    user = DbUser(user_id=user_id)
    # key = message.text
    key = message.text.replace('/edit ', '').strip()


    msg, entity = await get_message(key)

    if not msg:
        await bot.send_message(
            chat_id=user_id,
            text='Сообщение не найдено'
        )

        await user.set_state('')
        return

    await user.set_state(f'edit_{key}')

    await message.answer(f"Введите новый текст сообщения, \nстарый текст:\n", parse_mode='HTML')
    await message.answer(text=msg, entities=entity, parse_mode='HTML')


@admin.message(StateIs('edit_'))
async def editMessage(message: Message, bot: Bot) -> None:
    user = DbUser(user_id=message.from_user.id)
    state = await user.get_state()

    key = state.replace('edit_', '')
    msg = DbMessage(key=key)

    ms = await msg.select_message()
    if not ms:
        return

    entities = []

    if message.entities:
        for entity in message.entities:
            entities.append({
                'type': entity.type,
                'offset': entity.offset,
                'length': entity.length,
                'url': entity.url,
                'user': entity.user,
                'language': entity.language,
                'custom_emoji_id': entity.custom_emoji_id,
            })
    if message.caption_entities:
        for entity in message.caption_entities:
            entities.append({
                'type': entity.type,
                'offset': entity.offset,
                'length': entity.length,
                'url': entity.url,
                'user': entity.user,
                'language': entity.language,
                'custom_emoji_id': entity.custom_emoji_id,
            })

    # Save the message text and entities to the database
    await msg.update_record(
        text=message.html_text if message.html_text else message.caption,
        entity=json.dumps(entities)
    )
    await user.set_state('')

    await message.answer('Сообщение успешно изменено')


@admin.callback_query(F.data == 'set_price')
async def setPrice(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    user = DbUser(user_id=callback.from_user.id)
    await user.set_state('set_price')

    await bot.send_message(
        'Введите новую цену в формате: \nмес цена скидка\nЕсли скидки нету, то 0\nНовый тариф с новой строки\nПример: 1 125 0')


@admin.callback_query(F.data =='mailing')
async def mailing(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    user = DbUser(user_id=callback.from_user.id)
    await user.set_state('mailing')

    await bot.send_message(callback.from_user.id, 'Пришлите сообщение для рассылки' , reply_markup=get_back_kb())


@admin.callback_query(F.data =='list_promos')
async def listPromos(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    promos = await PromosSchema.query.gino.all()
    u = DbUser(user_id=callback.from_user.id)

    await bot.send_message(
        chat_id=u.user_id,
        text='Список промокодов:\n\n' + '\n'.join([f'{promo.name} - {promo.value}' for promo in promos])
    )


@admin.callback_query(F.data =='add_promo')
async def addPromo(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    user = DbUser(user_id=callback.from_user.id)
    await user.set_state('add_promo')

    await bot.send_message(callback.from_user.id, 'Введите промокод в формате: \nназвание скидка\nПример: promo 10')


@admin.message(StateIs('add_promo'))
async def setPromoHandler(message: Message, bot: Bot) -> None:
    user = DbUser(user_id=message.from_user.id)
    await user.set_state('')

    try:
        name, sale = message.text.split(' ')

        promo = await PromosSchema.query.where(PromosSchema.name == name).gino.first()

        if (promo):
            await promo.update(value=sale).apply()
            await message.answer(f'Промокод "{name}" обновлен до {sale}')
        else:
            await PromosSchema(name=name, value=sale).create()
            await message.answer(f'Промокод "{name}" создан')

    except Exception:
        await message.answer('Неверный формат')


@admin.callback_query(F.data == 'del_promo')
async def delPromo(callback: CallbackQuery, bot: Bot) -> None:
    await bot.answer_callback_query(callback.id, '')
    user = DbUser(user_id=callback.from_user.id)
    await user.set_state('del_promo')

    await bot.send_message(callback.from_user.id, 'Введите название удаляемого промокода')


@admin.message(StateIs('del_promo'))
async def deletePromoHandler(message: Message, bot: Bot) -> None:
    
    user = DbUser(user_id=message.from_user.id)
    await user.set_state('')
    #
    try:
        promo = await PromosSchema.query.where(PromosSchema.name == message.text).gino.first()

        if (promo):
            await promo.delete()
            await message.answer(f'Промокод "{message.text}" удален')
        else:
            await message.answer(f'Нет промокода "{message.text}"')

    except Exception:
        await message.answer('Неверный формат')


@admin.message(StateIs('mailing'))
async def mailingHandler(message: Message, bot: Bot) -> None:
    user = DbUser(user_id=message.from_user.id)

    await user.set_state('users_mailing')

    mes = await message.answer(
        'Пришлите ответом на сообщение для рассылки айди пользователей через пробел или 0 для всех', reply_markup=get_back_kb())

    mailing = MailingSchema(user_id=message.from_user.id, text=message.text, message_id=mes.message_id)
    await mailing.create()


@admin.message(StateIs('users_mailing'), lambda message: message.reply_to_message is not None)
async def mailingUsers(message: Message, bot: Bot) -> None:
    u = DbUser(user_id=message.from_user.id)

    users = message.text.split(' ') if ' ' in message.text else [message.text]
    message_id = message.reply_to_message.message_id

    if message.text != '0':
        for user_id in users:
            try:
                sent_msg = await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=message.from_user.id,
                    message_id=message_id,
                )
            except Exception:
                pass
    else:
        users = DbUser(role='user')
        users = await users.select_user()

        for user in users:
            try:
                sent_msg = await bot.copy_message(
                    chat_id=user.user_id,
                    from_chat_id=message.from_user.id,
                    message_id=message_id,
                )

                cur_user = DbUser(user_id=user.user_id)
            #    await cur_user.update_record(notification=1)
            except Exception:
                pass

    await u.set_state('')

    schema = DbUser()
    schema = await schema.get_schema()
    moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

    mailing = await MailingSchema.query.where(MailingSchema.message_id == message_id).gino.first()

    if mailing and moders:
        recepients = 'Всем пользователям' if message.text == '0' else f'Пользователям: {users}'

        for moder in moders:
            if (moder.user_id != message.from_user.id):
                await bot.send_message(
                    chat_id=moder.user_id,
                    text=f'Администратор {message.from_user.full_name} отправил рассылку с текстом: \n{mailing.text} \n\n{recepients}'
                )

    await message.answer('Рассылка завершена')


@admin.message(StateIs('set_price'))
async def setPrice(message: Message, bot: Bot) -> None:
    user = DbUser(user_id=message.from_user.id)

    try:
        months = message.text.split('\n')

        setting = {}

        for month in months:
            duration, price, sale = month.split(' ')
            setting[duration] = {
                'price': float(price),
                'sale': float(sale),
            }

        setting = json.dumps(setting)
        settings = DbSetting(key='prices')

        if not await settings.select_setting():
            new = DbSetting(key='prices', value=setting)
            await new.add()
        else:
            await settings.update_record(value=setting)

        await user.set_state('')

        await message.answer('Цена успешно изменена')
    except Exception:
        await message.answer('Неверный формат')


@admin.callback_query(lambda query: query.data.startswith('confirm_'))
async def confirm_handler(query: CallbackQuery, bot: Bot) -> None:

    user_id = int(query.data.split('_')[1])
    plan = int(query.data.split('_')[2])

    override_plan = int(query.data.split('_')[3]) if len(query.data.split('_')) > 3 else None

    pay = DbPay(user_id=user_id, status='pending', plan=str(plan))

    # We're assuming user only has one active pay and we update its duration indefinitely
    active_pay = DbPay(user_id=user_id, status='active')  # , plan=str(plan))

    active_pay_ = await active_pay.select_pay()
    pay_current = await pay.select_pay()

    link = None

    if (override_plan):
        plan = override_plan

    if active_pay_:
        await pay.remove()

        start_date = active_pay_.start_date if active_pay_.start_date else datetime.now()
        end_date = active_pay_.end_date if active_pay_.end_date else datetime.now()
        end_date += relativedelta(months=plan)

        duration = int(active_pay_.plan) + plan

        res = await active_pay.update_record(
            status='active',
            amount=active_pay_.amount + pay_current.amount,
            plan=str(duration),  # plan should always be a number of months
            start_date=start_date,
            end_date=end_date,
            remaining=0
        )


    else:
        if not pay_current:
            await query.answer('Ошибка')
            return
        else:
            if pay_current.status != 'pending':
                await query.answer('Ошибка')
                return
            elif pay_current.status == 'active':
                await bot.send_message(chat_id=query.from_user.id,
                                       text='Подписка уже была активирована. Сообщение об активации повторно отправлено пользователю')
                return

        await query.message.edit_reply_markup(reply_markup=None)

        start_date = datetime.now() if not pay_current.start_date else pay_current.start_date
        end_date = datetime.now() if not pay_current.start_date else pay_current.start_date

        end_date += relativedelta(months=plan)

        link = await bot.create_chat_invite_link(chat_id=-1002068661724, member_limit=1, name=str(user_id))

        res = await pay.update_record(status='active', plan=str(plan), start_date=start_date, end_date=end_date,
                                      remaining=0)

    schema = DbUser()
    schema = await schema.get_schema()
    moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

    if moders:
        for moder in moders:
            await bot.send_message(
                chat_id=moder.user_id,
                text=f'Администратор {query.from_user.full_name} подтвердил оплату пользователя {user_id} на {plan} мес'
            )

    evt = EventsSchema(
        user_id=str(moder.user_id),
        display_name=query.from_user.full_name,
        value=f"confirm_{user_id}_{plan}",
        callback="confirm",
        timestamp=datetime.now()
    )

    await evt.create()

    # await bot.send_message(
    #     chat_id=query.from_user.id,
    #     text='Оплата подтверждена'
    # )

    await bot.send_message(
        chat_id=user_id,
        text='Ваша оплата подтверждена, подписка активирована'
    )

    if link:
        await bot.send_message(
            chat_id=user_id,
            text=f'Добро пожаловать в клуб: {link.invite_link}'
        )

    await query.answer()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    'http://193.169.105.93:3001/cancel-reminders',
                    json={'user_id': user_id}
            ) as response:
                if response.status == 200:
                    print(f'Successfully cancelled reminders for user {user_id}')
                else:
                    print(f'Failed to cancel reminders for user {user_id}. Status code: {response.status}')
    except Exception as e:
        print(f'Error occurred while cancelling reminders: {e}')

    await query.answer('Оплата подтверждена и напоминания отменены.')

    try:
        await query.message.edit_reply_markup(reply_markup=None)
    except Exception:
        # it's okay if we can't edit the message
        pass


@admin.callback_query(lambda query: query.data.startswith('cancel_'))
async def cancel_handler(query: CallbackQuery, bot: Bot) -> None:
    
    user_id = int(query.data.split('_')[1])
    plan = int(query.data.split('_')[2])
    pay = DbPay(user_id=user_id, status='pending', plan=str(plan))
    pay_current = await pay.select_pay()

    if not pay_current:
        await query.answer('Ошибка')
        return

    await pay.update_record(status='canceled')

    # await bot.send_message(
    #     chat_id=query.from_user.id,
    #     text='Оплата отменена'
    # )

    schema = DbUser()
    schema = await schema.get_schema()
    moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

    if moders:
        for moder in moders:
            await bot.send_message(
                chat_id=moder.user_id,
                text=f'Администратор {query.from_user.full_name} отменил оплату пользователя {user_id} на {plan} мес'
            )

    await bot.send_message(
        chat_id=user_id,
        text='Ваша оплата отменена'
    )

    await query.answer()
    await query.message.edit_reply_markup(reply_markup=None)


@admin.message(F.content_type == 'video')
async def get_video_file_id(message: Message, bot: Bot) -> None:
    if message.caption and message.caption.lower() in ['about_club', 'enter_club']:
        file_id = message.video.file_id
        key = f"{message.caption.lower()}_video_id"

        db_setting = await SettingSchema.query.where(SettingSchema.key == key).gino.first()

        if db_setting:
            await db_setting.update(value=file_id).apply()
            await message.answer(f"Видео обновлено")
        else:
            id = 4 if message.caption.lower() == 'about_club' else 5

            new_setting = SettingSchema(id=id, key=key, value=file_id)
            await new_setting.create()
            await message.answer(f"Видео добавлено")

    else:
        await message.answer("Доступные ключи для видео: (about_club или enter_club)")


@admin.callback_query(F.data == 'manageuser')
async def manage_user_handler(callback: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback.id, '')
    await bot.send_message(callback.from_user.id, 'Введите id пользователя')
    user = DbUser(user_id=callback.from_user.id)

    await user.set_state('probiv')

@admin.message(StateIs('probiv'))
async def manage_user_handler(message: Message, bot: Bot) -> None:
    user_id = int(message.text)
    r = DbUser(message.from_user.id)

    user = DbUser(user_id=user_id)
    db_user = await user.select_user()

    if not db_user:
        await message.answer("Пользователь не найден.")
        await r.set_state('')
        return

    active_pay = await DbPay(user_id=user_id, status='active').select_pay()
    ended_pay = await DbPay(user_id=user_id, status='ended').select_pay()
    unpaid_pay = await DbPay(user_id=user_id, status='pending').select_pay()
    text = ''
    heading = f'{db_user.username}\n\n'
    print(1)
    if active_pay:
        text = f"Подписка закончится {active_pay.end_date}"
    elif ended_pay:
        text = f"Подписка закончилась {ended_pay.end_date}"
    elif unpaid_pay or not (active_pay or ended_pay):
        text = "У пользователя нет подписки"

    full_text = heading + text

    keyboard = get_manage_user_kb(user_id, bool(active_pay))
    await bot.send_message(message.from_user.id, full_text, reply_markup=keyboard, parse_mode='HTML')
    await r.set_state('')


@admin.callback_query(lambda query: query.data.startswith("add_months_"))
async def add_months_handler(query: CallbackQuery, bot: Bot) -> None:
    user_id, months = query.data.split('_')[2], query.data.split('_')[3]

    pay = DbPay(user_id=int(user_id), status='active')
    active_pay = await pay.select_pay()

    if active_pay:
        await active_pay.update(end_date = active_pay.end_date + relativedelta(months=int(months))).apply()

        schema = DbUser()
        schema = await schema.get_schema()
        moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

        if moders:
            for moder in moders:
                await bot.send_message(
                    chat_id=moder.user_id,
                    text=f'Администратор {query.from_user.full_name} продлил подписку пользователя {user_id} на {months} месяц(ев)'
                )
    else:
        await query.message.answer("У пользователя нет активной подписки")

    await query.answer()


@admin.callback_query(lambda query: query.data.startswith("activate_pay_"))
async def activate_pay_handler(query: CallbackQuery, bot: Bot) -> None:
    user_id, months = query.data.split('_')[2], query.data.split('_')[3]

    pay = DbPay(user_id=int(user_id), status='active', plan='default', name=query.from_user.full_name)
    pay.end_date = datetime.now() + relativedelta(months=int(months))
    await pay.add()

    schema = DbUser()
    schema = await schema.get_schema()
    moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

    if moders:
        for moder in moders:
            await bot.send_message(
                chat_id=moder.user_id,
                text=f'Администратор {query.from_user.full_name} активировал подписку пользователя {user_id} на {months} месяц(ев)'
            )

    await query.answer()


@admin.callback_query(lambda query: query.data.startswith("del_pay_"))
async def del_pay_handler(query: CallbackQuery, bot: Bot) -> None:
    user_id = query.data.split('_')[2]

    pay = DbPay(user_id=int(user_id), status='active')
    active_pay = await pay.select_pay()

    if active_pay:
        active_pay.status = 'ended'
        await active_pay.update(status='ended').apply()

        schema = DbUser()
        schema = await schema.get_schema()
        moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

        if moders:
            for moder in moders:
                await bot.send_message(
                    chat_id=moder.user_id,
                    text=f'Администратор {query.from_user.full_name} отменил подписку пользователя {user_id}'
                )
    else:
        await query.message.answer("У пользователя нет активной подписки")

    await query.answer()

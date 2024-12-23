import json
import os
import sys
import re
from datetime import datetime, timedelta
from aiogram.types.error_event import ErrorEvent
from filters.chat_type import ChatTypeFilter
from filters.role import RoleIs
from filters.state import StateIs
from typing import Tuple, List
from aiogram.types import MessageEntity
from keyboards.main import get_menu_kb, get_close_community_kb, get_club_kb, get_prices_kb, get_pay_kb, get_payed_kb, \
    get_confirm_kb, get_back_kb, main_menu, my_profile, get_utc_kb, change_language
import traceback
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile, MessageEntity, BotCommand, ReplyKeyboardRemove

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import math
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.utils.deep_linking import decode_payload

from middlewares.google_sheet import SheetMiddleware
from middlewares.update_online import UpdateOnlineMiddleware
from models.quick_commands import DbTeam, DbUser, DbMessage, DbSetting, DbPay
from models.schemas.promos import PromosSchema
from models.schemas.settings import SettingSchema

default_router = Router()

default_router.message.middleware(SheetMiddleware())
default_router.callback_query.middleware(SheetMiddleware())

default_router.message.middleware(UpdateOnlineMiddleware())
default_router.callback_query.middleware(UpdateOnlineMiddleware())

default_router.message.filter(
    ChatTypeFilter(chat_type="private")
)

ref_hash = {
    '0': 'g',
    '1': 'F',
    '2': 'k',
    '3': 'A',
    '4': 'z',
    '5': 'Y',
    '6': 'h',
    '7': 'D',
    '8': 'm',
    '9': 'T'
}

reverse_ref_hash = {v: k for k, v in ref_hash.items()}

def get_first_key_by_value(dictionary, value):
    return next((key for key, val in dictionary.items() if val == value), None)

def extract_referral_id(referral_link):
    referral_id = ""
    for i in referral_link:
        if i in reverse_ref_hash:
            referral_id += reverse_ref_hash[i]
    return referral_id

time_zones = {
    1: "UTC-12:00 (Baker Island Time)",
    2: "UTC-11:00 (Niue Time)",
    3: "UTC-10:00 (Hawaii-Aleutian Standard Time)",
    4: "UTC-9:00 (Alaska Standard Time)",
    5: "UTC-8:00 (Pacific Standard Time)",
    6: "UTC-7:00 (Mountain Standard Time)",
    7: "UTC-6:00 (Central Standard Time)",
    8: "UTC-5:00 (Eastern Standard Time)",
    9: "UTC-4:00 (Atlantic Standard Time)",
    10: "UTC-3:00 (Brasília Time)",
    11: "UTC-2:00 (South Georgia Time)",
    12: "UTC-1:00 (Azores Standard Time)",
    13: "UTC+0:00 (Greenwich Mean Time)",
    14: "UTC+1:00 (Central European Time)",
    15: "UTC+2:00 (Central Africa Time)",
    16: "UTC+3:00 (Moscow Time)",
    17: "UTC+4:00 (Gulf Standard Time)",
    18: "UTC+5:00 (Pakistan Standard Time)",
    19: "UTC+6:00 (Bangladesh Standard Time)",
    20: "UTC+7:00 (Indochina Time)",
    21: "UTC+8:00 (China Standard Time)",
    22: "UTC+9:00 (Japan Standard Time)",
    23: "UTC+10:00 (Australian Eastern Standard Time)",
    24: "UTC+11:00 (Magadan Time)",
    25: "UTC+12:00 (Fiji Time)"
}
@default_router.error()
async def error_handler(event: ErrorEvent, bot: Bot):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
    short_traceback = ''.join(formatted_traceback[-3:])  # get only last 3 lines
    error_info = f"⚠️ An error occurred: {event.exception}.\n\nStack trace:\n```{short_traceback}```"

    await bot.send_message(
        chat_id=7555401023,
        text=error_info,
        parse_mode='Markdown'
    )

    print(f"eror {event.exception}")
    traceback.print_exc()


async def get_message(key: str) -> Tuple[str, List[MessageEntity]]:
    msg = DbMessage(key=key)
    print(msg)
    msg = await msg.select_message()
    print(msg)
    entities = []
    try:
        entities_json = json.loads(msg.entity) if msg.entity else []
    except:
        entities_json = []


    for entity in entities_json:
        entities.append(MessageEntity(**entity))

    return (msg.text if msg.text else 'Сообщение не найдено'), entities


async def contact_handler(message: Message, bot: Bot, uid: int) -> None:
    user = DbUser(user_id=uid)
    await user.set_state('question')

    text, entity = await get_message('contact')

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(root_dir, 'media', 'contact.png')

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Attempt to send the photo
    await bot.send_photo(
        uid,
        photo=FSInputFile(file_path),
        caption=text,
        caption_entities=entity,
        reply_markup=get_back_kb()
    )


@default_router.message(CommandStart(deep_link=True))
async def start_handler(message: Message, command: CommandObject, bot: Bot) -> None:
    user = DbUser(user_id=message.from_user.id, role='user', username=message.from_user.username, name=message.from_user.full_name)

    if not await user.select_user():
        await user.add()

        referral_link = command.args

        # Приглашение по ссылке в команду
        if referral_link and referral_link.startswith('team_'):
            team_link = referral_link[5:]
            team_id = extract_referral_id(team_link)
            print(team_id)
            if user.user_id != team_id:
              team = await DbTeam(team_id=int(team_id)).select_team()
              if team:
                  pass
              #     #? нужно добавить столбец и записывать в него id команды в которой состоит user 
              #     # await DbUser(user_id=message.from_user.id).update_record(team_id=team_id)

                  # members = json.loads(team.members_id)
              #     if len(members) >= team.members_count:
              #         await message.answer("Команда уже заполнена.")
              #         return

              #     if message.from_user.id in members:
              #         await message.answer("Вы уже находитесь в этой команде.")
              #         return

              #     # Добавление пользователя в команду
              #     members.append(message.from_user.id)
              #     await DbTeam(team_id=team_id).update_record(members_id=json.dumps(members))
              #     await message.answer(f"Вы успешно добавлены в команду!")
              # else:
              #     await bot.send_message(message.from_user.id, "Команда не найдена")
              

        # Приглашение по ссылке
        if (referral_link) and not referral_link.startswith('team_'):
          inviter_id = extract_referral_id(referral_link)
          if user.user_id != inviter_id:
            await bot.send_message(message.from_user.id, f"Вы пришли по реферальной ссылке от пользователя ID: {inviter_id}")

            inviter_user = await DbUser(user_id=int(inviter_id)).select_user()
            if inviter_user:
                current_referals_count = inviter_user.referals_count
                new_referals_count = current_referals_count + 1
                await DbUser(user_id=int(inviter_id)).update_record(referals_count=new_referals_count)

        # Club
        if referral_link == 'club':
            text, entity = await get_message('private_community')
            video_setting = await SettingSchema.query.where(SettingSchema.key =='about_club_video_id').gino.first()

            video_id = video_setting.value if video_setting else 'BAACAgIAAxkBAAEBL61m4HxpcEZBsb6tEusFxepq56PsKQACRFMAAoHrCUuQW9rp0zVCJDYE'

            await bot.send_video(
                message.from_user.id,
                video=video_id,
                caption=text,
                caption_entities=entity,
                reply_markup=get_club_kb()
            )
        text, entity = await get_message('start')

        # Стартовое сообщение
        await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=main_menu())

        await bot.send_photo(
            message.from_user.id,
            photo=FSInputFile('media/start.png'),
            caption=text,
            caption_entities=entity,
            reply_markup=get_menu_kb(),
    )
    else:
      # Если пользователь уже был в бд, но по каким-то причинам удалял чат или блокировал бота
      await bot.send_message(message.from_user.id, 'С возвращением!', reply_markup=main_menu())

    

@default_router.message(CommandStart())
async def default_handler(message: Message, bot: Bot) -> None:
    user = DbUser(user_id=message.from_user.id)
    usr = await user.select_user()
    ans = 0

    # Если пользователь не существует, добавляем его
    if not usr:
        user = DbUser(
            user_id=message.from_user.id,
            role='user',
            username=message.from_user.username,
            name=message.from_user.full_name,
            parent=int(ans)
        )
        await user.add()
        usr = await user.select_user()
        
    commands = [
        BotCommand(
            command='/start',
            description='Начать работу'
        ),
        BotCommand(
            command='/help',
            description='Помощь'
        ),
        BotCommand(
            command='/pay',
            description='Оплатить подписку'
        ),
    ]

    await bot.set_my_commands(commands)

    text, entity = await get_message('start')
    await bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=main_menu())

    await bot.send_photo(
        message.from_user.id,
        photo=FSInputFile('media/start.png'),
        caption=text,
        caption_entities=entity,
        reply_markup=get_menu_kb(),
    )



@default_router.message(F.text == '👤Мой профиль')
async def profile_link(message: Message, bot: Bot):
    user = await DbUser(user_id=message.from_user.id).select_user()
    await DbUser(user_id=message.from_user.id).set_state('')
    if user.email is None:
        r = 'Не указано'
    else:
        r = user.email
    await bot.send_message(message.from_user.id, f'👤 Мой профиль\n\n— Telegram ID: {message.from_user.id}\n— Язык: {user.language}\n— Часовой пояс: {time_zones[13 + user.timezone]}\n— Почта: {r}', reply_markup=my_profile())


@default_router.message(F.text == '✉️Тарифные планы')
async def profile_link(message: Message, bot: Bot):
    await pay_handler(message, bot)


@default_router.message(F.text == '📝Моя подписка')
async def profile_link(message: Message, bot: Bot):
    user = await DbPay(user_id=message.from_user.id).select_pay()
    if user is None:
        ans = "— Вы еще не вступали в наш клуб, не упустите уникальную возможность, быть частью крупного сообщества трейдеров\n\n<i>Для оформления подписки перейдите в раздел: закрытое сообщество</i>"
        keyboard = get_menu_kb()
    else:
        if user.status == 'active':


            if user.start_date is not None:
                ans = f'<b>✅ Вы часть сильнейшего сообщества трейдеров Crypto Volium</b>\n\nВремя подписки {user.plan} месяц(а)\n\nВ сообществе с {(user.start_date).day}-{(user.start_date).month} {(user.start_date).year} года\nПодписка закончится {(user.end_date).day}-{(user.end_date).month} {(user.end_date).year} года\nПодиска закончится через'
            else:
                ans = f'<b>✅ Вы часть сильнейшего сообщества трейдеров Crypto Volium</b>\n\nПодписка закончится {(user.end_date).day}-{(user.end_date).month} {(user.end_date).year} года'
            keyboard = get_back_kb()
        else:
            ans = f'<b>❌ Ваша подписка закончилась</b>\n\nВы можете продлить её, возвращатесь, мы Вас ждём!\n\n<i>Для оформления подписки перейдите в раздел: закрытое сообщество</i>'
            keyboard = get_menu_kb()
    await bot.send_message(message.from_user.id, f'<b>🗃 Ваша подписка:</b>\n\n{ans}', reply_markup=keyboard, parse_mode='HTML')

async def send_profile_link(user_id: int, bot: Bot):
    invite_button = InlineKeyboardButton(text="Пригласить друга", callback_data="invite_friend")
    create_team_button = InlineKeyboardButton(text="Создать команду", callback_data="create_team")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[invite_button, create_team_button]])    
    await bot.send_message(user_id, "Выберите действие:", reply_markup=keyboard)

@default_router.message(F.text == '🔥Реферальная программа')
async def profile_link(message: Message, bot: Bot):
    await send_profile_link(message.from_user.id, bot)

@default_router.callback_query(F.data == 'invite_friend')
async def invite_friend(callback_query: CallbackQuery, bot: Bot):
    await DbUser(user_id=callback_query.from_user.id).set_state('')
    user = await DbUser(user_id=callback_query.from_user.id).select_user()
    referral_link = f"https://t.me/svmaster_bot?start="
    for i in str(user.user_id):
        referral_link += ref_hash[str(i)]

    reply_message = (
            f"🌟 Ваш персональный реферальный код: {referral_link} 🌟\n\n"
            f"Что такое рефералы?\n"
            f"Рефералы – это люди, которые присоединились к нашему клубу благодаря вашей рекомендации. Каждый приведенный друг может приносить вам вознаграждение!\n\n"
            f"📈 Ваши награды:\n"
            f"Вы можете просмотреть свои награды за рефералов по команде: /rewards\n\n"
            f"💰 Вознаграждение за приглашенное лицо:\n"
            f"За каждого реферала вы получаете 30% от суммы, которую он потратит. Вы можете выбрать, оставить все деньги себе или отдать часть как скидку вашему рефералу."
        )
    await callback_query.message.answer(reply_message)
    await callback_query.answer()

@default_router.callback_query(F.data == 'create_team')
async def create_team(callback_query: CallbackQuery, bot: Bot):
    
    await DbUser(user_id=callback_query.from_user.id).set_state('awaiting_team_creation')

    await callback_query.message.answer(
        "Введите максимальное количество участников в вашей команде (например, 4, 8, 12)."
    )
    await callback_query.answer()

@default_router.message(lambda msg: msg.text.isdigit())
async def finalize_team_creation(message: Message, bot: Bot):
    # Проверяем, находится ли пользователь в состоянии создания команды
    user = await DbUser(user_id=message.from_user.id).select_user()
    if user.state != 'awaiting_team_creation':
        await message.answer("Неверный этап процесса. Пожалуйста, начните с команды 'Создать команду'.")
        return

    max_members = int(message.text)
    if max_members < 1:
        await message.answer("Количество участников должно быть больше нуля.")
        return

    invite_link = f"https://t.me/svmaster_bot?start=team_"
    for i in str(user.user_id):
        invite_link += ref_hash[str(i)]

    # Создаем модель команды
    new_team = {
        "id": user.user_id,  # Уникальный ID команды (равен ID владельца)
        "invite_link": invite_link,
        "owner_id": user.user_id,
        "members_id": json.dumps([user.user_id]),  # Храним список участников как JSON-строку
        "members_count": max_members,
        "current_members": 1,
    }

    await DbTeam(team_id=user.user_id).add_team(**new_team)

    # Обновляем данные пользователя
    await DbUser(user_id=message.from_user.id).update_record(state='main_menu')

    # Подтверждение пользователю
    await message.answer(
        f"🎉 Команда успешно создана!\n\n"
        f"🌟 Ссылка для приглашения: {invite_link}\n"
        f"👥 Максимальное количество участников: {max_members}\n"
        f"🚀 Добавляйте участников и получайте бонусы!"
    )


@default_router.message(Command(commands=["rewards"]))
async def handle_awards_command(message: Message):
    user = await DbUser(user_id=message.from_user.id).select_user()
    
    reply_message = (
      f"Ваши достижения:\n"
      f"- Приведено рефералов: {user.referals_count}\n"
      f"- Активных рефералов в клубе: {user.active_referals}\n\n"
    )

    await message.answer(reply_message)

# @default_router.message(F.text == '🔥Реферальная программа')
# async def profile_link(message: Message, bot: Bot):
#    # user = DbUser(user_id=message.from_user.id).select_user()
#     await DbUser(user_id=message.from_user.id).set_state('')
#     user = await DbUser(user_id=message.from_user.id).select_user()
#     print('после этого')
#     print(user)
#     referral_link = f"https://t.me/CV_club_bot/start="
#     for i in str(user.user_id):
#         referral_link += ref_hash[str(i)]

#     reply_message = (
#             f"🌟 Ваш персональный реферальный код: {referral_link} 🌟\n\n"
#             f"Что такое рефералы?\n"
#             f"Рефералы – это люди, которые присоединились к нашему клубу благодаря вашей рекомендации. Каждый приведенный друг может приносить вам вознаграждение!\n\n"
#             f"Ваши достижения:\n"
#             f"- Приведено рефералов: {user.referals_count}\n"
#             f"- Активных рефералов в клубе: {user.active_referals}\n\n"
#             f"📈 Ваши награды:\n"
#             f"Вы можете просмотреть свои награды за рефералов по команде: /rewards\n\n"
#             f"💰 Вознаграждение за приглашенное лицо:\n"
#             f"За каждого реферала вы получаете 30% от суммы, которую он потратит. Вы можете выбрать, оставить все деньги себе или отдать часть как скидку вашему рефералу."
#         )
#     await message.answer(reply_message)
    
    
@default_router.callback_query(lambda query: query.data == 'jojoreference')
async def reference(query: CallbackQuery, bot: Bot) -> None:
    await DbUser(user_id=query.from_user.id).set_state('')
    await send_profile_link(query.from_user.id, bot)
    await bot.answer_callback_query(query.id, '')

@default_router.callback_query(lambda query: query.data == 'email')
async def email(query: CallbackQuery, bot: Bot) -> None:
    await bot.send_message(query.from_user.id, "👤 Мой аккаунт\n📝 Редактирование почты\nВведите E-mail в формате: customer@gmail.com", reply_markup=get_back_kb())
    await DbUser(user_id=query.from_user.id).set_state('Emailpull')
    await bot.answer_callback_query(query.id, '')

@default_router.callback_query(lambda query: query.data == 'language')
async def languge(query: CallbackQuery, bot: Bot) -> None:
    await DbUser(user_id=query.from_user.id).set_state('')
    await bot.send_message(query.from_user.id, "Выберите язык", reply_markup=change_language())
    await bot.answer_callback_query(query.id, '')



@default_router.message(StateIs('Emailpull'))
async def change_email(message: Message, bot: Bot):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Проверка с помощью регулярного выражения
    if re.match(pattern, str(message.text)):
        await bot.send_message(message.from_user.id, 'Успешно')
        await bot.delete_message(message.from_user.id, message.message_id)
        user = await DbUser(user_id=message.from_user.id).select_user()
        await DbUser(user_id=message.from_user.id).update_record(email=message.text)
        await bot.send_message(message.from_user.id, f'👤 Мой профиль\n\n— Telegram ID: {message.from_user.id}\n— Язык: {user.language}\n— Часовой пояс: {time_zones[13 + user.timezone]}\n— Почта: {message.text}', reply_markup=my_profile())
        await DbUser(user_id=message.from_user.id).set_state('')
    else:
        await bot.send_message(message.from_user.id, 'Введите E-mail в формате: customer@yourmail.com')



@default_router.callback_query(lambda query: (query.data)[:5] == 'lang_')
async def change_lang(query: CallbackQuery, bot: Bot) -> None:
    await bot.send_message(query.from_user.id, "Успешно !")
    await DbUser(user_id=query.from_user.id).update_record(languge=(query.data)[5:])
    await bot.answer_callback_query(query.id, '')
    await bot.delete_message(query.from_user.id, query.message.message_id)

@default_router.callback_query(lambda query: (query.data)[:4] == 'utc_')
async def change_utc(query: CallbackQuery, bot: Bot) -> None:
    await bot.send_message(query.from_user.id, "Успешно !")
    data = query.data.split('_')
    r = int(data[2])
    if data[1] == '0':
        r *= -1
    print(data[2], data[1])
    await DbUser(user_id=query.from_user.id).update_record(timezone=r)
    await bot.answer_callback_query(query.id, '')
    await bot.delete_message(query.from_user.id, query.message.message_id)



@default_router.callback_query(lambda query: query.data == 'timezone')
async def languge(query: CallbackQuery, bot: Bot) -> None:
    await bot.send_message(query.from_user.id, "Выберите часовой пояс", reply_markup=get_utc_kb())
    await bot.answer_callback_query(query.id, '')


@default_router.message(Command('help'))
async def help_handler(message: Message, bot: Bot) -> None:
    await contact_handler(message, bot, message.from_user.id)


@default_router.message(Command('pay'))
async def pay_handler(message: Message, bot: Bot) -> None:
    prices = DbSetting(key='prices')
    prices = await prices.select_setting()

    text, entity = await get_message('select_plan')

    video_setting = await SettingSchema.query.where(SettingSchema.key =='enter_club_video_id').gino.first()

    video_id = video_setting.value if video_setting else 'BAACAgIAAxkBAAEBMaxm4YxWO8g6CZ0RZDX68_L-TPxlxAACcVQAAh63EUvgbsvWnpwEKDYE'

    await bot.send_video(
        message.from_user.id,
        video=video_id,
        caption=text,
        caption_entities=entity,
        reply_markup=get_prices_kb(
            json.loads(prices.value) if prices else {}
        )
    )


@default_router.message(Command('botmoncheck'))
async def help_handler(message: Message, bot: Bot) -> None:
    await bot.send_message(
        message.from_user.id,
        text='running'
    )


@default_router.callback_query(lambda query: query.data == 'contact')
async def contact_handler_query(query: CallbackQuery, bot: Bot) -> None:
    await contact_handler(query.message, bot, query.from_user.id)

    await query.answer()
    await query.message.delete_reply_markup()


@default_router.callback_query(lambda query: query.data == 'education')
async def education_handler(query: CallbackQuery, bot: Bot) -> None:
    text, entity = await get_message('education')
    # await bot.send_message(
    #     query.from_user.id,
    #     text=text,
    #     entities=entity,
    #     reply_markup=get_close_community_kb(),
    # )

    await bot.send_photo(
        query.from_user.id,
        photo=FSInputFile('media/education.png'),
        caption=text,
        caption_entities=entity,
        reply_markup=get_close_community_kb(),
    )

    await query.answer()


@default_router.callback_query(lambda query: query.data == 'about_club')
async def about_club_handler(query: CallbackQuery, bot: Bot) -> None:
    text, entity = await get_message('private_community')

    video_setting = await SettingSchema.query.where(SettingSchema.key =='about_club_video_id').gino.first()

    video_id = video_setting.value if video_setting else 'BAACAgIAAxkBAAEBL61m4HxpcEZBsb6tEusFxepq56PsKQACRFMAAoHrCUuQW9rp0zVCJDYE'

    await bot.send_video(
        query.from_user.id,
        video=video_id,
        caption=text,
        caption_entities=entity,
        reply_markup=get_club_kb()
    )

    await query.answer()


@default_router.callback_query(lambda query: query.data == 'private_community')
async def private_community_handler(query: CallbackQuery, bot: Bot) -> None:
    await bot.send_chat_action(query.from_user.id, 'upload_video')

    video_setting =  await SettingSchema.query.where(SettingSchema.key =='about_club_video_id').gino.first()

    video_id = video_setting.value if video_setting else 'BAACAgIAAxkBAAEBL61m4HxpcEZBsb6tEusFxepq56PsKQACRFMAAoHrCUuQW9rp0zVCJDYE'

    text, entity = await get_message('private_community')
    await bot.send_video(
        query.from_user.id,
        video=video_id,
        caption=text,
        caption_entities=entity,
        reply_markup=get_club_kb()
    )

    await query.answer()


@default_router.callback_query(lambda query: query.data == 'enter_club')
async def enter_club_handler(query: CallbackQuery, bot: Bot) -> None:
    prices = DbSetting(key='prices')
    prices = await prices.select_setting()

    text, entity = await get_message('select_plan')

    video_setting =  await SettingSchema.query.where(SettingSchema.key =='enter_club_video_id').gino.first()

    video_id = video_setting.value if video_setting else 'BAACAgIAAxkBAAEBMaxm4YxWO8g6CZ0RZDX68_L-TPxlxAACcVQAAh63EUvgbsvWnpwEKDYE'

    await bot.send_video(
        query.from_user.id,
        video=video_id,
        caption=text,
        caption_entities=entity,
        reply_markup=get_prices_kb(
            json.loads(prices.value) if prices else {}
        )
    )

    await query.answer()


@default_router.callback_query(lambda query: query.data == 'promo_code')
async def promo_code_handler(query: CallbackQuery, bot: Bot) -> None:
    user = DbUser(user_id=query.from_user.id)

    await bot.send_message(
        query.from_user.id,
        'Введите промокод ответом на это сообщение',
    )

    await user.set_state('promo_code')

    await query.answer()


@default_router.message(StateIs('promo_code'))
async def promo_code_reply_handler(message: Message, bot: Bot) -> None:
    user = DbUser(user_id=message.from_user.id)
    await user.set_state('')

    promo = await PromosSchema.query.where(PromosSchema.name == message.text).gino.first()

    if not promo:
        await message.answer('Промокод не найден')
        return

    prices = DbSetting(key='prices')
    prices = await prices.select_setting()
    prices_value = json.loads(prices.value) if prices else {}

    promo_sale = promo.value

    if promo_sale and float(promo_sale) > 0:
        for key in prices_value.keys():
            prices_value[key]['sale'] = promo_sale

        await message.answer('Промокод принят')

        text, entity = await get_message('select_plan')

        video_setting = await SettingSchema.query.where(SettingSchema.key =='enter_club_video_id').gino.first()

        video_id = video_setting.value if video_setting else 'BAACAgIAAxkBAAEBMaxm4YxWO8g6CZ0RZDX68_L-TPxlxAACcVQAAh63EUvgbsvWnpwEKDYE'

        await bot.send_video(
            message.from_user.id,
            video=video_id,
            # Use the file_id of the video
            caption=text,
            caption_entities=entity,
            reply_markup=get_prices_kb(
                prices_value
            )
        )
    else:
        text, entity = await get_message('promo_code_not')

        await bot.send_message(
            message.from_user.id,
            text=text,
            entities=entity,
        )


@default_router.callback_query(lambda query: query.data.startswith('pay_'))
async def pay_handler1(query: CallbackQuery, bot: Bot) -> None:
    price = float(query.data.split('_')[1])
    tariff = query.data.split('_')[2]
    pay = DbPay(user_id=query.from_user.id, amount=price,
                plan=tariff, status='disabled', username=query.from_user.username, name=query.from_user.full_name) # добавляем в бд строку о подписке
    pay_current = await pay.select_pay()

    active_pay = DbPay(user_id=query.from_user.id,
                       status='active', plan=tariff)
    active_pay_current = await active_pay.select_pay()
    active_pays = await active_pay.get_pay_by_status_and_user_id(user_id=query.from_user.id, status='active')

    if active_pays:
        plans = [plan.plan for plan in active_pays]

        if tariff not in plans and active_pay_current:
            await query.answer('У вас уже есть активная подписка')
            return

    if not pay_current:
        await pay.add()

    text, entity = await get_message('pay')
    await bot.send_photo(
        query.from_user.id,
        photo=FSInputFile('media/wallet.png'),
        caption=text,
        caption_entities=entity,
    )

    await bot.send_message(
        query.from_user.id,
        f'Вы выбрали тариф: {tariff} мес за ${price}',
        reply_markup=get_pay_kb(tariff)
    )

    await query.answer()


@default_router.callback_query(lambda query: query.data == 'payed')
async def payed_handler(query: CallbackQuery) -> None:
    await query.message.edit_reply_markup(reply_markup=get_payed_kb())

    user = DbUser(user_id=query.from_user.id)
    pay = DbPay(user_id=query.from_user.id, status='disabled')

    text, entity = await get_message('payed')
    await query.message.edit_text(
        text=text,
        entities=entity,
    )

    await user.set_state('payed')
    await pay.update_record(status='not_payed', username=query.from_user.username)

    await query.answer()


@default_router.message(StateIs('payed'), lambda message: message.photo is not None)
async def photo_handler(message: Message, bot: Bot) -> None:
    await message.answer('Ожидайте подтверждения!')

    user = DbUser(user_id=message.from_user.id)
    pay = DbPay(user_id=message.from_user.id, status='not_payed')
    plan = await pay.select_pay()
    plan = plan.plan

    await pay.update_record(status='pending', username=message.from_user.username)

    admin = DbUser(role='admin')
    admins = await admin.select_user()

    for admin in admins:
        # await bot.forward_message(admin.user_id, message.chat.id, message.message_id)
        text = f'{message.from_user.id}\n<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>\n\n{message.text if message.text else message.caption}'

        await bot.send_photo(
            chat_id=admin.user_id,
            photo=message.photo[-1].file_id,
            caption=text,
            parse_mode='HTML',
        )

        prices = DbSetting(key='prices')
        prices = await prices.select_setting()

        await bot.send_message(
            admin.user_id,
            f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a> отправил фото оплаты - {plan} мес',
            parse_mode='HTML',
            reply_markup=get_confirm_kb(message.from_user.id, plan, json.loads(prices.value) if prices else {})
        )

    await user.set_state('')


@default_router.callback_query(lambda query: query.data == 'back')
async def back_handler(query: CallbackQuery, bot: Bot) -> None:
    await query.message.delete()
    user = DbUser(user_id=query.from_user.id)
    # prices = DbSetting(key='prices')
    # prices = await prices.select_setting()

    # text, entity = await get_message('select_plan')

    # await bot.send_photo(
    #     query.from_user.id,
    #     photo=FSInputFile('media/happy.png'),
    #     caption=text,
    #     caption_entities=entity,
    #     reply_markup=get_prices_kb(
    #         json.loads(prices.value) if prices else {}
    #     )
    # )

    text, entity = await get_message('start')
    await user.set_state('')
    await bot.send_photo(
        query.from_user.id,
        photo=FSInputFile('media/start.png'),
        caption=text,
        caption_entities=entity,
        reply_markup=get_menu_kb(),
    )


@default_router.message(RoleIs(['user']), StateIs('question'), lambda message: message.reply_to_message is not None)
async def contact_reply_handler(message: Message, bot: Bot) -> None:
    schema = DbUser()
    schema = await schema.get_schema()

    moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

    if moders:
        for user in moders:
            # await bot.forward_message(user.user_id, message.chat.id, message.message_id)

            text = f'{message.from_user.id}\n<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>\n\n{message.text if message.text else message.caption}'

            # type of message
            if message.photo:
                await bot.send_photo(
                    chat_id=user.user_id,
                    photo=message.photo[-1].file_id,
                    caption=text,
                    parse_mode='HTML',
                )
            else:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=text,
                    parse_mode='HTML',
                )

    # await message.answer('Ваш вопрос отправлен модераторам, ожидайте ответа')


@default_router.message(RoleIs(['user']))
async def contact_reply_handler(message: Message, bot: Bot) -> None:
    schema = DbUser()
    schema = await schema.get_schema()

    moders = await schema.query.where(schema.role.in_(['admin', 'moder'])).gino.all()

    if moders:
        for user in moders:
            # await bot.forward_message(user.user_id, message.chat.id, message.message_id)
            # await bot.send_message(
            #     chat_id=user.user_id,
            #     text=f'{message.from_user.id}\n<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>\n\n{message.text}',
            # )

            text = f'{message.from_user.id}\n<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>\n\n{message.text if message.text else message.caption}'

            # type of message
            if message.photo:
                await bot.send_photo(
                    chat_id=user.user_id,
                    photo=message.photo[-1].file_id,
                    caption=text,
                    parse_mode='HTML',
                )
            else:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=text,
                    parse_mode='HTML',
                )

    # await message.answer('Ваш вопрос отправлен модераторам, ожидайте ответа')

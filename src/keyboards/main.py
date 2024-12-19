from aiogram.utils.i18n import gettext as _
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import math


# def get_menu_kb() -> ReplyKeyboardMarkup:
#     builder = ReplyKeyboardBuilder()
#     builder.button(text='/start'))
#     # return builder.as_markup(resize_keyboard=True)
def main_menu() -> ReplyKeyboardMarkup:

    button1 = KeyboardButton(text="👤Мой профиль")
    button2 = KeyboardButton(text="📝Моя подписка")
    button3 = KeyboardButton(text="🔥Реферальная программа")
    button4 = KeyboardButton(text="✉️Тарифные планы")
    keyboard = ReplyKeyboardMarkup(keyboard=[
            [button1, button2],  # Первая строка
            [button3, button4],   # Вторая строка
        ], resize_keyboard=True)
    return keyboard


def my_profile():
       kb = InlineKeyboardBuilder()
    #   kb.row(InlineKeyboardButton(text='Реферальная программма',
     #        callback_data='utc_0_0'))
       kb.row(InlineKeyboardButton(text='🔥 Реферальная программа', callback_data='jojoreference'),
           InlineKeyboardButton(text='🌎 Язык', callback_data='language'))
       kb.row(InlineKeyboardButton(text='⏰ Часовой пояс', callback_data='timezone'),
           InlineKeyboardButton(text='📥 Почта', callback_data='email'))
       return kb.as_markup()    
  
def change_language():
       kb = InlineKeyboardBuilder()
    #   kb.row(InlineKeyboardButton(text='Реферальная программма',
     #        callback_data='utc_0_0'))
       kb.row(InlineKeyboardButton(text='🇷🇺 Русский язык', callback_data='lang_ru'))
       kb.row(InlineKeyboardButton(text='Назад', callback_data='back'))

       return kb.as_markup()    


def get_utc_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='UTC+0:00 - Greenwich Mean Time (GMT), Iceland',
           callback_data='utc_0_0'))
    kb.row(InlineKeyboardButton(text='UTC+1:00 - Central European Time (Poland, Germany)', callback_data='utc_1_1'),
           InlineKeyboardButton(text='UTC-1:00 - Azores, Cape Verde', callback_data='utc_0_1'))
    kb.row(InlineKeyboardButton(text='UTC+2:00 - Eastern European Time (Greece, Ukraine)', callback_data='utc_1_2'),
           InlineKeyboardButton(text='UTC-2:00 - South Georgia, South Sandwich Islands', callback_data='utc_0_2'))
    kb.row(InlineKeyboardButton(text='UTC+3:00 - Moscow Time, Saudi Arabia', callback_data='utc_1_3'),
           InlineKeyboardButton(text='UTC-3:00 - Argentina, Brazil (some regions)', callback_data='utc_0_3'))
    kb.row(InlineKeyboardButton(text='UTC+4:00 - Samara Time, United Arab Emirates', callback_data='utc_1_4'),
           InlineKeyboardButton(text='UTC-4:00 - Atlantic Time (Puerto Rico, Nova Scotia)', callback_data='utc_0_4'))
    kb.row(InlineKeyboardButton(text='UTC+5:00 - Uzbekistan, Pakistan', callback_data='utc__15'),
           InlineKeyboardButton(text='UTC-5:00 - Eastern Time (New York, Toronto)', callback_data='utc_0_5'))
    kb.row(InlineKeyboardButton(text='UTC+6:00 - Kazakhstan, Bangladesh', callback_data='utc_1_6'),
           InlineKeyboardButton(text='UTC-6:00 - Central Time (Texas, Mexico)', callback_data='utc_0_6'))
    kb.row(InlineKeyboardButton(text='UTC+7:00 - Indonesia, Vietnam', callback_data='utc_1_7'),
           InlineKeyboardButton(text='UTC-7:00 - Mountain Time (Colorado, Arizona)', callback_data='utc_0_7'))
    kb.row(InlineKeyboardButton(text='UTC+8:00 - China, Singapore', callback_data='utc_1_8'),
           InlineKeyboardButton(text='UTC-8:00 - Pacific Time (California, British Columbia)', callback_data='utc_0_8'))
    kb.row(InlineKeyboardButton(text='UTC+9:00 - Japan, South Korea', callback_data='utc_1_9'),
           InlineKeyboardButton(text='UTC-9:00 - Alaska (excluding Aleutian Islands)', callback_data='utc_0_9'))
    kb.row(InlineKeyboardButton(text='UTC+10:00 - Australia (eastern regions), Papua New Guinea', callback_data='utc_1_10'),
           InlineKeyboardButton(text='UTC-10:00 - Hawaii, Aleutian Islands (UTC-10)', callback_data='utc_0_10'))
    kb.row(InlineKeyboardButton(text='UTC+11:00 - Solomon Islands, Magadan', callback_data='utc_1_11'),
           InlineKeyboardButton(text='UTC-11:00 - American Samoa, Niue', callback_data='utc_0_11'))
    kb.row(InlineKeyboardButton(text='UTC+12:00 - Fiji, Kiribati', callback_data='utc_1_12'),
           InlineKeyboardButton(text='UTC-12:00 - Baker Island, Howland Island', callback_data='utc_0_12'))
    kb.row(InlineKeyboardButton(text='Назад', callback_data='back'))
    return kb.as_markup()    
    

def get_manage_user_kb(user_id: int, has_active_pay: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    if has_active_pay:
        kb.row(InlineKeyboardButton(text='Добавить 1 месяц', callback_data=f'add_months_{user_id}_1'))
        kb.row(InlineKeyboardButton(text='Добавить 3 месяца', callback_data=f'add_months_{user_id}_3'))
        kb.row(InlineKeyboardButton(text='Добавить 6 месяцев', callback_data=f'add_months_{user_id}_6'))
        kb.row(InlineKeyboardButton(text='Отменить подписку', callback_data=f'del_pay_{user_id}'))
    else:
        kb.row(InlineKeyboardButton(text='Активировать 1 месяц', callback_data=f'activate_pay_{user_id}_1'))
        kb.row(InlineKeyboardButton(text='Активировать 3 месяца', callback_data=f'activate_pay_{user_id}_3'))
        kb.row(InlineKeyboardButton(text='Активировать 6 месяцев', callback_data=f'activate_pay_{user_id}_6'))

    return kb.as_markup()


def get_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Закрытое сообщество',
           callback_data='private_community'))
    kb.row(InlineKeyboardButton(text='Обучение', callback_data='education'),
           InlineKeyboardButton(text='Связь', callback_data='contact'))

    return kb.as_markup()




def get_close_community_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Подробнее о клубе', callback_data="about_club"), )

    return kb.as_markup()


def get_club_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Да, хочу вступить!', callback_data='enter_club'))
    kb.row(InlineKeyboardButton(text='Больше подробностей', url="http://cryptovolium.online/ru"))

    return kb.as_markup()


def get_prices_kb(prices: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for key, value in prices.items():
        price = float(value['price'])
        sale = float(value['sale'])
        new_price = math.ceil(price - price * sale / 100) if sale > 0 else price
        kb.row(InlineKeyboardButton(text=f'{key} мес: ${price}' + (f' -> ${new_price} (-{sale} %)' if sale > 0 else ''),
                                    callback_data=f'pay_{new_price}_{key}'))

    kb.row(InlineKeyboardButton(text='Ввести промокод', callback_data='promo_code'))

    return kb.as_markup()

def get_pay_kb(tariff: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    pay_url = 'https://t.me/tribute/app?startapp=saZh' if tariff == '1' else 'https://teletype.in/@crypto.volium/oplata-bank-card'

    kb.row(InlineKeyboardButton(text='Я оплатил', callback_data='payed'),
           InlineKeyboardButton(text='Оплата с карты', url= pay_url))
    kb.row(InlineKeyboardButton(text='Связь', callback_data='contact'),
              InlineKeyboardButton(text='Назад', callback_data='back'))

    return kb.as_markup()

def get_payed_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Связь', callback_data='contact'),
              InlineKeyboardButton(text='Назад', callback_data='back'))

    return kb.as_markup()


def get_confirm_kb(user_id: int, plan: str, prices: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm_{user_id}_{plan}'),
           InlineKeyboardButton(text='Отмена', callback_data=f'cancel_{user_id}_{plan}'))

    for key, value in prices.items():
        kb.row(InlineKeyboardButton(text=f'Подтвердить {key} мес.', callback_data=f'confirm_{user_id}_{plan}_{key}'))

    return kb.as_markup()


def get_back_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Назад', callback_data='back'))

    return kb.as_markup()

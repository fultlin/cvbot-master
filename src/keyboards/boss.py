from aiogram.utils.i18n import gettext as _
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import math


# def get_menu_kb() -> ReplyKeyboardMarkup:
#     builder = ReplyKeyboardBuilder()
#     builder.button(text='/start'))
#     # return builder.as_markup(resize_keyboard=True)



def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='🔊🟩 Рассылка', callback_data='mailing', resize_keyboard=True)],
        [InlineKeyboardButton(text='👀🟩 Ричауты', callback_data='reach_out', resize_keyboard=True)],
        [InlineKeyboardButton(text='👀🟩 Изменить наполнение', callback_data='edit_text', resize_keyboard=True)],
        [InlineKeyboardButton(text='👀🟩 Изменить фото сообщения', callback_data='edit_photo', resize_keyboard=True)],
        [InlineKeyboardButton(text='📊🟪 Посмотреть промокоды', callback_data='list_promos', resize_keyboard=True)],
        [InlineKeyboardButton(text='📊🟪 Добавить промокод', callback_data='add_promo', resize_keyboard=True)],
        [InlineKeyboardButton(text='🧩🟨 Информация о подписчике', callback_data='manageuser', resize_keyboard=True)],
     #   [InlineKeyboardButton(text='🔇⬛️ Забанить/разбанить челика', callback_data='ban', resize_keyboard=True)],
        [InlineKeyboardButton(text='🔇⬛️ Задать цену', callback_data='set_price', resize_keyboard=True)],
        [InlineKeyboardButton(text='🔇⬛️ Удалить промокод', callback_data='del_promo', resize_keyboard=True)],
    #    [InlineKeyboardButton(text='🔳🔲 Назначить/снять администратора', callback_data='sds', resize_keyboard=True)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list, row_width=2)


def get_reach_out(j: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Покинули клуб в текущем месяце', callback_data=f'rec_0_0_{j}'))
    kb.row(InlineKeyboardButton(text='Покинули клуб после 1 месяца подписки', callback_data=f'rec_1_0_{j}'))
    kb.row(InlineKeyboardButton(text='Покинули клуб после 2-3 месяцев подписки', callback_data=f'rec_2_0_{j}'))
    kb.row(InlineKeyboardButton(text='Покинули клуб после 4 и более месяцев подписки', callback_data=f'rec_3_0_{j}'))
    kb.row(InlineKeyboardButton(text='Глянуть всех', callback_data=f'rec_4_0_{j}'))
    kb.row(InlineKeyboardButton(text='Назад', callback_data='admin'))
    return kb.as_markup()


def get_etap_out(i: str, j: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Нулевая категория', callback_data=f'gro_{i}_0_{j}'))
    kb.row(InlineKeyboardButton(text='Первая категория', callback_data=f'gro_{i}_1_{j}'))
    kb.row(InlineKeyboardButton(text='Вторая категория', callback_data=f'gro_{i}_2_{j}'))
    kb.row(InlineKeyboardButton(text='Третья категория', callback_data=f'gro_{i}_3_{j}'))
    kb.row(InlineKeyboardButton(text='Назад', callback_data='reach_out'))
    return kb.as_markup()


def set_reach_pout(user_id: int, username : str, table: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='First reachout', callback_data=f'dda_0_{user_id}_{table}'),
  InlineKeyboardButton(text='2nd reachout', callback_data=f'dda_1_{user_id}_{table}'))
    kb.row(InlineKeyboardButton(text='3rd reachout', callback_data=f'dda_2_{user_id}_{table}'),
    InlineKeyboardButton(text='Вернется позже', callback_data=f'dda_3_{user_id}_{table}'))
    kb.row(InlineKeyboardButton(text='Кастомная категория', callback_data=f'dda_6_{user_id}_{table}'))
    kb.row(InlineKeyboardButton(text='Вернулся', callback_data=f'dda_4_{user_id}_{table}'),
InlineKeyboardButton(text='Отказался', callback_data=f'dda_5_{user_id}_{table}'))
    kb.row(InlineKeyboardButton(text='Написать', url=f't.me/{username}'))
    kb.row(InlineKeyboardButton(text='Назад', callback_data='reach_out'))
    return kb.as_markup()



####Клавиатура для книжки перелистываемая принимает индекс пейдж в хендлерах ес че возвращается рекурсивно

def boss_mark(t: str, j: str, numpage: str, users: list ) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if users is not None:
        

        numpage = int(numpage)
        pages = len(users) // 10 + 1  # определяем количество страниц
        print(pages)
        numpage = max(0, min(numpage, pages - 1))  # ограничиваем значение счетчика до границ страниц
        start = numpage * 10  # определяем начало и конец страницы
        end = start + 10
        for i in range(start, end):
            try:
                if users[i].username is not None:
                    kb.row(InlineKeyboardButton(text=f'{users[i].username}', callback_data=f'ri_{users[i].user_id}_{t}_{j}'))
            except:
                break
        if numpage > 0:
            kb.row(InlineKeyboardButton(text="Назад", callback_data=f'rec_{t}_{j}_{numpage - 1}'))
        if numpage < pages - 1:
            kb.row(InlineKeyboardButton(text="Вперед", callback_data=f'rec_{t}_{j}_{numpage + 1}'))
    kb.row(InlineKeyboardButton(text='Выйти', callback_data=f'reach_out'))
    return kb.as_markup()
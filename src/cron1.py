import asyncio
from models.db_gino import connect_to_db
from models.quick_commands import DbPay, DbUser, DbMessage, DbRecent, FirstRecent, SecondRecent, ThirdRecent
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
from io import BytesIO
import telebot
from telebot.types import InputMediaPhoto
from handlers.default import get_message
from aiogram.types import Message, CallbackQuery, FSInputFile, MessageEntity, BotCommand
import time
import threading

def send_voice_message(chat_id, voice_file, delay):
    import config
    time.sleep(delay)  # Задержка в секундах
    with open(voice_file, 'rb') as voice:
        bot = telebot.TeleBot(config.BOT_TOKEN)
        bot.send_voice(chat_id=chat_id, voice=voice)


async def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    load_dotenv(base_dir / '.env')

    import config

    await connect_to_db()

    bot = telebot.TeleBot(config.BOT_TOKEN)

    u_db = DbUser()
    users = await u_db.select_users_by_notification_and_role(-1, 'user')

    pay = DbPay()

    #print(f"[cron] processing {len(users)} users pending notification")

    admins = await u_db.get_users_by_role('admin')
    r = await u_db.get_users_by_role('user')
    reply_markup = telebot.types.InlineKeyboardMarkup()
    reply_markup.add(telebot.types.InlineKeyboardButton(
        text='Вступить в клуб', callback_data='enter_club'))


  #  members = list()
  #  members_res = list()
  #  for y in r:
   #     i = DbPay(user_id=y.user_id)
    #    if not await i.select_pay():
     #       continue
        
      #  members.append((i.user_id, bot.get_chat_member(-1002068661724, i.user_id).status))
       # if bot.get_chat_member(-1002068661724, i.user_id).status != 'left':
        #    if bot.get_chat(i.user_id).username not in norm:
         #       members_res.append(bot.get_chat(i.user_id).id)

    #real_member_id = list()
    #for i in pays:
    #    if i.username not in norm:
     #       real_member_id.append(i.user_id)
        
    #ans = set(members_res) - set(real_member_id)
    #print(ans)
    #for i in ans:
     #   try:
      #      bot.kick_chat_member(-1002068661724, i)
       #     print(i)
       # except:
        #    print(1)
 
    # print(*members)
    # Get follow-up messages
    follow_up_15m_text, follow_up_15m_entity = await get_message('follow_up_15m')
    follow_up_1h_text, follow_up_1h_entity = await get_message('follow_up_1h')
    follow_up_2h_text, follow_up_2h_entity = await get_message('follow_up_2h')
    follow_up_1d_text, follow_up_1d_entity = await get_message('follow_up_1d')
    follow_up_2d_text, follow_up_2d_entity = await get_message('follow_up_2d')
    follow_up_3d_text, follow_up_3d_entity = await get_message('follow_up_3d')
    follow_up_4d_text, follow_up_4d_entity = await get_message('follow_up_4d')
    follow_up_10d_text, follow_up_10d_entity = await get_message('follow_up_10d')
    #Заполнение никнеймов
    
   # for user in r:
       # e = DbUser(user_id=user.user_id)
      #  p = DbPay(user_id=user.user_id)
     #   chat = bot.get_chat(user.user_id)
        #usr = chat.username
        #name = str(chat.first_name) + ' ' + str(chat.last_name)
       # print(name, user.user_id)
      #  await e.update_record(username=usr, name=name)
     #   a = await p.get_pay_by_user_id(user.user_id)
    #    if a:
       #     await p.update_record(username=usr, name=name)
 
    # Process each user and send notifications based on their offline time
    for user in users:
        offline_time = (datetime.now() - user.last_online).total_seconds()
        notification_flag = 0
        print(user.user_id, offline_time, user.notification)
        if user.notification != -1: 
            try:
                if offline_time > 60 * 14400 and user.notification == 7:
                    bot.send_photo(user.user_id, 
                                     photo="https://ibb.org.ru/1/qUkGgq",
                                     caption=follow_up_10d_text, 
                                     reply_markup=reply_markup,
        
                                     parse_mode='HTML')
                    notification_flag = -1
                if offline_time > 60 * 5760 and user.notification == 6:
                    bot.send_photo(user.user_id, 
                                     photo="https://ibb.org.ru/1/fbx1zl",
                                     caption=follow_up_4d_text, 
                                     reply_markup=reply_markup,
        
                                     parse_mode='HTML')
                    notification_flag = 7
                if offline_time > 60 * 4320 and user.notification == 5:
                    
                    bot.send_photo(user.user_id, 
                                     photo="https://ibb.org.ru/1/fbxQlg",
                                     caption=follow_up_3d_text, 
                                     reply_markup=reply_markup,
                    
                                     parse_mode='HTML')
                    notification_flag = 6
                elif offline_time > 60 * 2880 and user.notification == 4:
                    bot.send_photo(user.user_id, 
                                     photo="https://ibb.org.ru/1/fbxMRF",
                                     caption=follow_up_2d_text, 
                                     reply_markup=reply_markup,
                     
                                     parse_mode='HTML')
                    notification_flag = 5
                elif offline_time > 60 * 1440 and user.notification == 3:
                    photo_urls = [
                                'https://ibb.org.ru/1/qU7J36',
                                'https://ibb.org.ru/1/qU72wM',
                                'https://ibb.org.ru/1/qU7en3'
                            ]

    # Список для хранения объектов InputFile
                    media = []
                    d = True
                    # Загружаем фото по URL и добавляем в список media
                    for url in photo_urls:
                        try:
                            current_image_file = url
                           # photo.name = url.split("/")[-1]  # Устанавливаем имя файла
                            if d:
                                media.append(telebot.types.InputMediaPhoto(media=current_image_file, caption=follow_up_1d_text, parse_mode='HTML'))    
                                d = False 
                            else:
                                media.append(telebot.types.InputMediaPhoto(media=current_image_file))
                        except requests.exceptions.RequestException as e:
                            print(f"Ошибка при загрузке изображения {url}: {e}")



                    # Отправляем сообщения с фотографиями
                    print(media)
                    if media:
                        


            # Отправляем сообщения с фотографиями
                        bot.send_media_group(chat_id=user.user_id, media=media)

                       # except Exception as e:
       #  bot.send_photo(user.user_id, 
                 #                    photo="https://imgur.com/a/vVpDtWq",
                 #                    caption=follow_up_1d_text, 
                 #                    reply_markup=reply_markup,
                        
                  #                   parse_mode='HTML')
                  
                  
                    voice_file1 = 'media/voice1.ogg'  # Замените на путь к вашему аудиофайлу
                    voice_file2 = 'media/voice2.ogg' 
    # Запускаем отдельный тред для отправки сообщения через 10 минут (600 секунд)
                    threading.Thread(target=send_voice_message, args=(user.user_id, voice_file1, 600)).start()
                    threading.Thread(target=send_voice_message, args=(user.user_id, voice_file2, 600)).start()
                    notification_flag = 4
                elif offline_time > 60 * 120 and user.notification == 2:
                    bot.send_message(user.user_id,
                                     text=follow_up_2h_text,
                                     reply_markup=reply_markup,
                                     entities=follow_up_2h_entity,
                                     parse_mode='HTML')
                    notification_flag = 3

                elif offline_time > 60 * 60 and user.notification == 1:
                    bot.send_message(user.user_id,
                                     text=follow_up_1h_text,
                                     reply_markup=reply_markup,
                                     entities=follow_up_1h_entity,
                                     parse_mode='HTML')
                    notification_flag = 2

                elif offline_time > 60 * 15 and user.notification < 1:
                    bot.send_message(user.user_id,
                                     text=follow_up_15m_text,
                                     reply_markup=reply_markup,
                                     entities=follow_up_15m_entity,
                                     parse_mode='HTML')
                    notification_flag = 1

                # Update notification flag in the database if notification was sent
                if notification_flag:
                    cur_user = DbUser(user_id=user.user_id)
                    await cur_user.update_record(notification=notification_flag)

            except Exception as e:
                error_message = str(e)
                if "Error code: 403" in error_message and "bot was blocked by the user" in error_message:
                    print(f"Bot was blocked by the user with ID: {user.user_id}")
                    cur_user = DbUser(user_id=user.user_id)
                    await cur_user.update_bot_blocked(True)
                    await cur_user.update_record(notification=-1)
                else:
                    print(f"An error occurred: {error_message}")



if __name__ == '__main__':
    asyncio.run(main())

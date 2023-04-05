from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove
from keyboards import menu_keyboard
from db import connect_to_db

reply_markup = InlineKeyboardMarkup(menu_keyboard)


def say_hi(update, context):
    '''Получаем информацию о чате, из которого пришло сообщение,
    сохраняем в переменную chat'''
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я бот компании Micepartner!\nВыберите команду:',
                             reply_markup=reply_markup)


def start(update, context):
    '''Получаем информацию о чате, из которого пришло сообщение,
    сохраняем в переменную chat'''
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Выберите команду:', reply_markup=reply_markup)


def get_contact(update, context):
    chat_id = update.effective_chat.id
    contact = update.message.contact
    if contact and contact.user_id == update.message.from_user.id:
        reply_markup_remove = ReplyKeyboardRemove()
        context.bot.send_message(chat_id=chat_id,
                                 text="Спасибо!Загружаю данные.",
                                 reply_markup=reply_markup_remove)
        phone_number = contact.phone_number
        print(phone_number[1:])
        mydb, mycursor = connect_to_db()
        sql1 = f"SELECT surname, name, fathername, id FROM dp_users WHERE phoneMobile LIKE '%{phone_number[1:]}' ORDER BY id  DESC "
        mycursor.execute(sql1)
        user_fullname = mycursor.fetchone()
        user_id = user_fullname[3]
        sql2 = f"SELECT country.name as country, region.name as region, city.name as city, phoneMobile, email, job, address, dp_specialties.name as specialty FROM dp_users LEFT JOIN city on city.id=dp_users.cityRus LEFT JOIN region on region.id=dp_users.regionRus LEFT JOIN country on country.id=dp_users.countryMice LEFT JOIN dp_specialties on dp_specialties.id = dp_users.specialty1 WHERE dp_users.id = {user_id}"
        mycursor.execute(sql2)
        user_contact = mycursor.fetchone()
        print(user_contact)

        if user_fullname:
            full_name = user_fullname[0] + ' ' + user_fullname[1] + ' ' + user_fullname[2]
            # speciality = result[3]
            message_text = (f"""<b>Личный кабинет</b>\n\n<b>{full_name}</b>\nID:{user_fullname[3]}\n{user_contact[-1]}\n\n{user_contact[2]}\n{user_contact[3]}\n{user_contact[4]}\n{user_contact[5]}\n{user_contact[6]}\n""")
            context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')
        else:
            context.bot.send_message(chat_id=chat_id,
                                     text="Пользователь не найден.")
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text="Вы отправили чужой контакт!")

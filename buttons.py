from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.parsemode import ParseMode
from db import connect_to_db
from keyboards import contact_keyboard
import time
import datetime


def button_events(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id,
                             text='Выберите тип мероприятия',
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Онлайн', callback_data='online'),
                                                                 InlineKeyboardButton('Оффлайн',
                                                                                      callback_data='offline')
                                                                 ]]))


def button_online(update, context):
    chat_id = update.effective_chat.id
    mydb, mycursor = connect_to_db()
    # # Получаем текущее Unix время
    current_time = int(time.time())
    # # Запрашиваем данные из базы данных
    sql = "SELECT DISTINCT themes, dateOn, url FROM dp_events WHERE dateOn > %s and city LIKE '%нлайн%' and url is not null ORDER BY dateOn"
    mycursor.execute(sql, (current_time,))
    myresult = mycursor.fetchall()
    # # Формируем список мероприятий
    events_list = ''
    for x in myresult:
        date_time = datetime.datetime.fromtimestamp(x[1])
        events_list += '&#128214 {} \n&#128467 Дата: {} \n &#127760 <a href="{}">Страница мероприятия</a> \n\n'.format(x[0], date_time.strftime(
            "%d-%m-%Y"), x[2])
    # # Отправляем список мероприятий
    context.bot.send_message(chat_id=chat_id, text=events_list, parse_mode=ParseMode.HTML)


def button_offline(update, context):
    chat_id = update.effective_chat.id
    mydb, mycursor = connect_to_db()
    # # Получаем текущее Unix время
    current_time = int(time.time())
    # # Запрашиваем данные из базы данных
    sql = "SELECT DISTINCT themes, dateOn, url FROM dp_events WHERE dateOn > %s and city NOT LIKE '%нлайн%' and url is not null ORDER BY dateOn"
    mycursor.execute(sql, (current_time,))
    myresult = mycursor.fetchall()
    # # Формируем список мероприятий
    events_list = ''
    for x in myresult:
        date_time = datetime.datetime.fromtimestamp(x[1])
        events_list += '&#128214 {} \n&#128467 Дата: {} \n &#127760 <a href="{}">Страница мероприятия</a> \n\n'.format(x[0], date_time.strftime(
            "%d-%m-%Y"), x[2])
    # # Отправляем список мероприятий
    context.bot.send_message(chat_id=chat_id, text=events_list, parse_mode=ParseMode.HTML)


def button_lk(update, context):
    chat_id = update.effective_chat.id
    custom_keyboard = [[contact_keyboard]]
    reply_markup_lk = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=chat_id,
                             text="Для входа необходимо авторизоваться. Для этого нажмите кнопку 'Поделиться контактом'",
                             reply_markup=reply_markup_lk)
    return "WAITING_CONTACT"


def button_support(update, context):
    query = update.callback_query
    user = query.from_user
    query.answer()
    query.edit_message_text(f'Присоединяйтесь к группе техподдержки: https://t.me/+NI-a_LiklBI2MWUy\n{user.first_name}, вы можете задать свой вопрос там.')


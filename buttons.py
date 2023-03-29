from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ParseMode
from db import connect_to_db
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
    context.bot.send_message(chat_id,
                             text='Выберите тип мероприятия',
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Онлайн', callback_data='online'),
                                                                 InlineKeyboardButton('Оффлайн',
                                                                                      callback_data='offline')
                                                                 ]]))
    mydb, mycursor = connect_to_db()
    # # Получаем текущее Unix время
    current_time = int(time.time())
    # # Запрашиваем данные из базы данных
    sql = "SELECT DISTINCT themes, dateOn, url FROM dp_events WHERE dateOn > %s and city LIKE '%нлайн%' and url is not null ORDER BY dateOn"
    mycursor.execute(sql, (current_time,))
    myresult = mycursor.fetchall()
    # print(myresult)
    # # Формируем список мероприятий
    events_list = ''
    for x in myresult:
        date_time = datetime.datetime.fromtimestamp(x[1])
        events_list += '{} \nДата: {} \n <a href="{}">Страница мероприятия</a> \n\n'.format(x[0], date_time.strftime(
            "%d-%m-%Y"), x[2])
    # # Отправляем список мероприятий
    context.bot.send_message(chat_id=chat_id, text=events_list, parse_mode=ParseMode.HTML)


def button_lk(update, context):
    chat_id = update.effective_chat.id
    contact_keyboard = KeyboardButton('\U0001F4DE Поделиться контактом', request_contact=True, web_app=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=chat_id,
                             text="Поделитесь своим контактом, пожалуйста?",
                             reply_markup=reply_markup)

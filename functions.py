import datetime
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
        mydb, mycursor = connect_to_db()
        sql1 = f"SELECT surname, name, fathername, id FROM dp_users WHERE phoneMobile LIKE '%{phone_number[1:]}' ORDER BY id  DESC "
        mycursor.execute(sql1)
        result = mycursor.fetchall()
        if len(result) > 1:
            context.bot.send_message(chat_id=chat_id,
                                     text="У вас обнаружено несколько аккаунтов. Необходимо написать в техподдержку.")
            return
        elif len(result) == 1:
            # обработка случая, когда есть только одна запись
            user_fullname = result[0]
            user_id = user_fullname[3]
            sql2 = f"SELECT country.name as country, region.name as region, city.name as city, phoneMobile, email, job, address, dp_specialties.name as specialty FROM dp_users LEFT JOIN city on city.id=dp_users.cityRus LEFT JOIN region on region.id=dp_users.regionRus LEFT JOIN country on country.id=dp_users.countryMice LEFT JOIN dp_specialties on dp_specialties.id = dp_users.specialty1 WHERE dp_users.id = {user_id}"
            mycursor.execute(sql2)
            user_contact = mycursor.fetchone()
            sql3 = f"""SELECT 
              de.dateOff as date,
              dc.number,
              de.mpcert,
              de.themes as eventname,
              dc.credits,
              dc.id,
              dc.fedcode,
              de.sfe1,
              dc.fedbonus,
              fs.time as time,
              de.mintime as mintime
              FROM 
              dp_certificates dc 
              LEFT JOIN dp_events de ON dc.eventId = de.id
              LEFT JOIN dp_users du ON dc.userId = du.id
              LEFT JOIN (SELECT
              table1.eid,
              table1.uid,
              COUNT(DISTINCT table1.tic) AS time
              FROM 
              (        
                SELECT
                  uid,
                  eid,
                  CONCAT(eid,'.',uid,'.',HOUR(time),':',MINUTE(time)) as tic
                FROM 
                  fa_statistic fs, 
                  dp_events de 
                WHERE 
                  FROM_UNIXTIME(de.dateOn) < fs.time AND 
                  FROM_UNIXTIME(de.dateOff) > fs.time AND 
                  de.id IN (SELECT eventId FROM dp_certificates dc WHERE dc.userId = '{user_id}') AND 
                  fs.eid IN (SELECT eventId FROM dp_certificates dc WHERE dc.userId = '{user_id}') AND
                  fs.uid = '{user_id}' AND
                  fs.control = 1
              ) AS table1 GROUP BY eid) AS fs ON dc.userId = fs.uid AND dc.eventId = fs.eid 
              WHERE 
                userId = '{user_id}'
                ORDER BY de.dateOff DESC"""
            mycursor.execute(sql3)
            user_serts = mycursor.fetchall()
            if user_fullname:
              full_name = user_fullname[0] + ' ' + user_fullname[1] + ' ' + user_fullname[2]
              # speciality = result[3]
              message_text = (
                  f"""<b>Личный кабинет</b>\n\n<b>{full_name}</b>\nID:{user_fullname[3]}\n{user_contact[-1]}\n\n &#x1F4CD {user_contact[2]}\n &#128222 {user_contact[3]}\n &#9993 {user_contact[4]}\n &#128188 {user_contact[5]}\n &#127970 {user_contact[6]}\n\n""")
              context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')
              cert_list = ''
              if not user_serts:
                  context.bot.send_message(chat_id=chat_id, text='Список мероприятий пуст', parse_mode='HTML')
              else:
                  for x in user_serts:
                      date_time = datetime.datetime.fromtimestamp(x[0])
                      cert_list += f'<b>Ваши коды НМО:</b>\n\n&#128467<b>Дата</b>:\n {date_time.strftime("%d-%m-%Y")} \n&#128214<b>Название</b>\n {x[3]} \n <b>Ваш ИКП:</b>\n {x[6]} \n\n'
                  context.bot.send_message(chat_id=chat_id, text=cert_list, parse_mode='HTML')
              now = datetime.datetime.now()
              current_time = now.strftime("%H:%M %d.%m.%Y")
              with open('logs.txt', 'a', encoding='utf-8') as file:
                  file.write(f'date: {current_time}, user_info: {user_fullname}, user_id: {user_id}\n')
        else:
            context.bot.send_message(chat_id=chat_id,
                                    text="Необнаружен аккаунт в базе данных. Можно написать в техподдержку.")
            return
    else:
      context.bot.send_message(chat_id=chat_id,
                              text="Вы отправили чужой контакт!")

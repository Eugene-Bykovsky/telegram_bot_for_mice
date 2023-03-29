from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove
from keyboards import menu_keyboard
from buttons import button_lk

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
        # обрабатываем полученный контакт
        # Делаем запрос в базу и показываем сертификат
        # удаляем клавиатуру
        # context.bot.send_message(chat_id=chat_id,
        #                         text="Спасибо за ваш контакт!",
        #                         reply_markup=reply_markup_remove)
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text="Вы отправили чужой контакт!")


# def send_message(message):
#     bot.send_message(chat_id, message)

# send_message('The Matrix has you')

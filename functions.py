from telegram import InlineKeyboardMarkup
from keyboards import menu_keyboard

reply_markup = InlineKeyboardMarkup(menu_keyboard, resize_keyboard=True)


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

# def send_message(message):
#     bot.send_message(chat_id, message)

# send_message('The Matrix has you')

import os

from telegram import Bot
from telegram.ext import Updater, Filters, MessageHandler

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')  # Добавьте токен в код (не делайте так в реальных проектах!)
chat_id = os.getenv('CHAT_ID')  # Укажите chat_id

### ОТПРАВКА СООБЩЕНИЙ ###

# экземпляр класса для исх.сообщений
bot = Bot(token)

# def send_message(message):
#     bot.send_message(chat_id, message)

# send_message('The Matrix has you')


### ОБРАБОТКА ВХОДЯЩИХ СООБЩЕНИЙ ###

# экземпляр класса для вх.сообщений
updater = Updater(token)

def say_hi(update, context):
    '''Получаем информацию о чате, из которого пришло сообщение,
    сохраняем в переменную chat'''
    chat = update.effective_chat
    # В ответ на любое текстовое сообщение 
    # будет отправлено 'Привет, я ...!'
    context.bot.send_message(chat_id=chat.id, text='Привет, я бот компании Micepartner!')

# Регистрируется обработчик MessageHandler;
# из всех полученных сообщений он будет выбирать только текстовые сообщения
# и передавать их в функцию say_hi()
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

# Метод start_polling() запускает процесс polling, 
# приложение начнёт отправлять регулярные запросы для получения обновлений.
updater.start_polling()
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle() 
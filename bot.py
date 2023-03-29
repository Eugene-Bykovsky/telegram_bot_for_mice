import os

from telegram import Bot
from telegram.ext import Updater, Filters, MessageHandler, CallbackQueryHandler, CommandHandler

from dotenv import load_dotenv
from buttons import button_events, button_online, button_lk
from functions import say_hi, start

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('CHAT_ID')

### ОТПРАВКА СООБЩЕНИЙ ###
# экземпляр класса для исх.сообщений
bot = Bot(token)

### ОБРАБОТКА ВХОДЯЩИХ СООБЩЕНИЙ ###
# экземпляр класса для вх.сообщений
updater = Updater(token)

# обработчики
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
updater.dispatcher.add_handler(CallbackQueryHandler(button_events, pattern='events'))
updater.dispatcher.add_handler(CallbackQueryHandler(button_online, pattern='online'))
updater.dispatcher.add_handler(CallbackQueryHandler(button_lk, pattern='lk'))
updater.dispatcher.add_handler(CommandHandler('start', start))

# Метод start_polling() запускает процесс polling, 
# приложение начнёт отправлять регулярные запросы для получения обновлений.
updater.start_polling()
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle()
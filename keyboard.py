from telegram import InlineKeyboardButton

keyboard = [[InlineKeyboardButton("Мероприятия", callback_data='events')],
            [InlineKeyboardButton("Личный кабинет", callback_data='lk')],
            [InlineKeyboardButton("Трансляция", callback_data='stream')],
            [InlineKeyboardButton("Трансфер", callback_data='transfer')],
            [InlineKeyboardButton("Тех.поддержка", callback_data='support')],
            ]

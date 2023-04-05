from telegram import InlineKeyboardButton, KeyboardButton

menu_keyboard = [[InlineKeyboardButton("Мероприятия", callback_data='events')],
            [InlineKeyboardButton("Личный кабинет", callback_data='lk')],
            [InlineKeyboardButton("Трансляция", callback_data='stream')],
            [InlineKeyboardButton("Трансфер", callback_data='transfer')],
            [InlineKeyboardButton("Техподдержка", callback_data='support')],
            ]

contact_keyboard = KeyboardButton('\U0001F4DE Поделиться контактом', request_contact=True)
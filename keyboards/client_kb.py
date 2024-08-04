from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# keyboard for client
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

b_help = KeyboardButton('/help')
b_info = KeyboardButton('/info')

kb_client.add(b_help)
kb_client.add(b_info)
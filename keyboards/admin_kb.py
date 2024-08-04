from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# keyboard for admin
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

b_admin_logout = KeyboardButton('/admin_logout')

kb_admin.add(b_admin_logout)
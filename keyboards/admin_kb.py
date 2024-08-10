from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# keyboard for admin
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(KeyboardButton('/send_logs_manually'))
kb_admin.add(KeyboardButton('/admin_logout'))

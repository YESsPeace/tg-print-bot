from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# keyboard for client
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(KeyboardButton('/Приветствие'))
kb_client.add(KeyboardButton('/Изменить_цвет_печати'))

color_choosing_kb = InlineKeyboardMarkup(resize_keyboard=True)

black_and_white = InlineKeyboardButton(text='Черно-белая', callback_data="color_preset_0")
colored = InlineKeyboardButton(text='Цветная', callback_data="color_preset_1")

color_choosing_kb.insert(black_and_white)
color_choosing_kb.insert(colored)
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config import dp, bot, logger, color_preset
from keyboards import kb_client, color_choosing_kb

import requests

from functions import send_logs_auto, print_image

import pickle

class FSMClient(StatesGroup):
    pass

@dp.message_handler(commands=['start', 'Приветствие'])
async def command_start(message: types.Message):
    try:
        await message.answer(
        f"""
Привет, я бот, который помогает с печатью. Просто скиньте мне ваши файлы.
Сейчас выбрана {"цветная" if color_preset else "черно-белая"} печать.
/change_color_preset - Чтобы изменить цвет печати.
        """,
        reply_markup=kb_client
        )

    except Exception as e:
        logger.error(f"command_start: {e}")
        await send_logs_auto(e)

@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    try:
        photo = message.photo[-1]

        # Получаем изображение как байтовый объект
        file_id = photo.file_id

        image_url = f"https://api.telegram.org/bot{bot._token}/getFile?file_id={file_id}"
        response = requests.get(image_url)
        image_path = response.json()['result']['file_path']
        image_data = requests.get(f"https://api.telegram.org/file/bot{bot._token}/{image_path}").content

        await print_image(image=image_data, colored=color_preset)
    
    except Exception as e:
        logger.error(f"get_photo: {e}")
        await send_logs_auto(e)

@dp.message_handler(commands=['Изменить_цвет_печати', 'change_color_preset'])
async def ask_color_preset(message: types.Message):
    try:
        await message.answer(
            'Выберете тип печати',
            reply_markup=color_choosing_kb
        )
    
    except Exception as e:
        logger.error(f"ask_color_preset: {e}")
        await send_logs_auto(e)

@dp.callback_query_handler(lambda c: c.data.startswith('color_preset'))
async def set_color_preset(callback_query: types.CallbackQuery):
    try:
        global color_preset

        color_preset = bool(int(callback_query.data.split('_')[-1]))

        with open("color_preset.pickle", "wb") as file:
            pickle.dump(color_preset, file)

        await bot.send_message(
            callback_query.from_user.id,
            text=
            f'Хорошо, теперь выбрана {"цветная" if color_preset else "черно-белая"} печать.\n' + \
            f'Просто скиньте фото или группу фотография, а я их напечатаю.'
        )
    
    except Exception as e:
        logger.error(f"set_color_preset: {e}")
        await send_logs_auto(e)



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'Приветствие'])
    dp.register_message_handler(ask_color_preset, commands=['Изменить_цвет_печати', 'change_color_preset'])
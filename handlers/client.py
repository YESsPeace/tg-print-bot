from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config import dp, bot, logger, color_preset
from keyboards import kb_client, color_choosing_kb

import requests

from functions import send_logs_auto, print_image


class FSMClient(StatesGroup):
    pass

@dp.message_handler(commands=['start', 'Перезапустить'])
async def command_start(message: types.Message):
    await message.answer(
        f"""
'Привет, я бот, который помогает с печатью. Просто скиньте мне ваши файлы.'
/change_color_preset - Чтобы изменить цвет печати, сейчас выбрана {"цветная" if color_preset else "черно-белая"} печать.
        """,
        reply_markup=kb_client
    )

@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):

    photo = message.photo[-1]

    # Получаем изображение как байтовый объект
    file_id = photo.file_id

    image_url = f"https://api.telegram.org/bot{bot._token}/getFile?file_id={file_id}"
    response = requests.get(image_url)
    image_path = response.json()['result']['file_path']
    image_data = requests.get(f"https://api.telegram.org/file/bot{bot._token}/{image_path}").content

    await print_image(image=image_data, colored=color_preset)

@dp.message_handler(commands=['Изменить_цвет_печати', 'change_color_preset'])
async def ask_color_preset(message: types.Message):
    await message.answer(
        'Выберете тип печати',
        reply_markup=color_choosing_kb
    )

@dp.callback_query_handler(lambda c: c.data.startswith('color_preset'))
async def set_color_preset(callback_query: types.CallbackQuery):
    global color_preset

    color_preset = bool(int(callback_query.data.split('_')[-1]))

    await bot.send_message(
        callback_query.from_user.id,
        text=
        f'Хорошо, теперь выбрана {"цветная" if color_preset else "черно-белая"} печать.\n' + \
        f'Просто скиньте фото или группу фотография, а я их напечатаю.'
    )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'Перезапустить'])
    dp.register_message_handler(ask_color_preset, commands=['Изменить_цвет_печати', 'change_color_preset'])
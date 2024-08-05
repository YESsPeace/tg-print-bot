from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp, bot, logger
from keyboards import kb_client

import requests

from functions import send_logs_auto, print_image


class FSMClient(StatesGroup):
    pass


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(
        'Привет, я бот, который помогает с печатью. Просто скиньте мне ваши файлы.',
        reply_markup=kb_client
    )

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    try:
        photo = message.photo[-1]

        # Получаем изображение как байтовый объект
        file_id = photo.file_id

        image_url = f"https://api.telegram.org/bot{bot._token}/getFile?file_id={file_id}"
        response = requests.get(image_url)
        image_path = response.json()['result']['file_path']
        image_data = requests.get(f"https://api.telegram.org/file/bot{bot._token}/{image_path}").content

        # await bot.send_photo(message.chat.id, photo=image_data)

        await print_image(image=image_data)

    except Exception as e:
        logger.error(f"handle_photo: {e}")
        await send_logs_auto(e)



# TODO: make description about all commands 
@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.answer(
        'help_message',
        reply_markup=kb_client
    )


# TODO: add info about admin (site, github and other)
@dp.message_handler(commands=['info'])
async def command_info(message: types.Message):
    await message.answer(
        'info_message',
        reply_markup=kb_client
    )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_info, commands=['info'])
    dp.register_message_handler(command_help, commands=['help'])
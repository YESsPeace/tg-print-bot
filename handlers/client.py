from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp, bot
from keyboards import kb_client


class FSMClient(StatesGroup):
    pass


# TODO: make implementation of the main task - printing
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(
        'Привет, я бот, который помогает с печатью. Просто скиньте мне ваши файлы.',
        reply_markup=kb_client
    )


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
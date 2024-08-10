from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp, bot, admins_ids, logger

from keyboards import kb_admin

from functions import send_logs_auto


class FSMAdmin(StatesGroup):
    admin = State()


@dp.message_handler(commands=['admin_login'])
async def admin_login(message: types.Message, state: FSMContext):
    """
    Вход в админку. Проверяет id пользователя, если он дминский, то впускает.
    """
    try:
        await message.answer(
            'Проверяем вас на админа...',
        )

        user_id = str(message.from_user.id)
        full_name = message.from_user.full_name

        if user_id in admins_ids:
            await FSMAdmin.admin.set()

            await message.answer(
                f'Добро пожаловать в панель администратора, {full_name}',
                reply_markup=kb_admin
            )

        else:
            await message.answer(
                f'Извините, но вы, {full_name}, не админ. Я вызываю полицию',
            )

    except Exception as e:
        logger.error(f"admin_login: {e}")
        await send_logs_auto(e)



@dp.message_handler(commands=['admin_logout'], state=FSMAdmin.admin)
async def admin_logout(message: types.Message, state: FSMContext):
    """
    Выход из админки
    """
    try:
        await state.finish()

        full_name = message.from_user.full_name

        await message.answer(
            f'Выход из панели администратора успешен. Пока-пока, {full_name}',
        )

    except Exception as e:
        logger.error(f"admin_logout: {e}")
        await send_logs_auto(e)

@dp.message_handler(commands=['send_logs_manually'], state=FSMAdmin.admin)
async def send_logs_manually(message: types.Message):
    """
    Вручную отправляет логги. Логги отправляются в лс того, кто вызвал.

    :param message: Сообщение, что выслал пользователь
    :type message: aiogram.types.Message
    """
    try:
        await message.answer(
            'Отправляю логги...',
        )

        with open('main_log.log', 'rb') as log_file:
            await bot.send_document(
                chat_id=message.chat.id,
                document=log_file)

    except FileNotFoundError as e:
        logger.error(f"send_logs_manually: logs file is not found {e}")

        # creating of logs file
        with open('main_log.log', "w"):
            pass

        logger.info(f"send_logs_manually: logs file created with the name 'main_log.log', because the upper Error {e}")

    except Exception as e:
        logger.error(f"send_logs_manually: {e}")
        await send_logs_auto(e)

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_login, commands=['admin_login'])
    dp.register_message_handler(admin_logout, commands=['admin_logout'], state=FSMAdmin.admin)
    dp.register_message_handler(admin_logout, commands=['send_logs_manually'], state=FSMAdmin.admin)

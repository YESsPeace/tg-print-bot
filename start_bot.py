from aiogram.utils import executor

from config import dp
from functions import check_logs_size_and_delete

from handlers import register_handlers_client, register_handlers_admin


async def on_startup(_):
    await check_logs_size_and_delete('main_log.log')
    print('Bot started')


register_handlers_client(dp)
register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
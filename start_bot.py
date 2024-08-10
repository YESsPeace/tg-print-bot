import os

from aiogram.utils import executor

from config import dp
from functions import check_logs_size_and_delete

from handlers import register_handlers_client, register_handlers_admin

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    clear_console()
    welcome_art = r"""
   d888888o.   8888888 8888888888 8 8888      88 8 888888888o.       8 8888          .8.                    8 888888888o.
 .`8888:' `88.       8 8888       8 8888      88 8 8888    `^888.    8 8888         .888.                   8 8888    `^888.
 8.`8888.   Y8       8 8888       8 8888      88 8 8888        `88.  8 8888        :88888.                  8 8888        `88.
 `8.`8888.           8 8888       8 8888      88 8 8888         `88  8 8888       . `88888.                 8 8888         `88
  `8.`8888.          8 8888       8 8888      88 8 8888          88  8 8888      .8. `88888.                8 8888          88
   `8.`8888.         8 8888       8 8888      88 8 8888          88  8 8888     .8`8. `88888.               8 8888          88
    `8.`8888.        8 8888       8 8888      88 8 8888         ,88  8 8888    .8' `8. `88888.              8 8888         ,88
8b   `8.`8888.       8 8888       ` 8888     ,8P 8 8888        ,88'  8 8888   .8'   `8. `88888.             8 8888        ,88'
`8b.  ;8.`8888       8 8888         8888   ,d8P  8 8888    ,o88P'    8 8888  .888888888. `88888.            8 8888    ,o88P'
 `Y8888P ,88P'       8 8888          `Y88888P'   8 888888888P'       8 8888 .8'       `8. `88888.           8 888888888P'
                                        
                                        Бот для печати изображений на принтере для Иры
    """
    print(welcome_art)

async def on_startup(_):
    await check_logs_size_and_delete('main_log.log')
    print("Готово! Бот успешно запущен.")
    print("Чтобы выключить, закройте окно.")

print_welcome_message()
print("Запуск бота...")

register_handlers_client(dp)
register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
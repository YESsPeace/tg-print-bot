import os

import aiogram.bot as Bot

from config import logger, bot, admins_ids

async def send_logs_auto(exception: Exception):
    """
    Автоматически отправляет логги в лс всех админов, при каких-либо ошибках.
    Логги админов храняться в перменой admins_ids в config.py и берутся из переменных окружения.

    :param exception: Ошибка, которая вынудила вызвать функцию.
    :type exception: Exception
    """
    try:
        with open('.\main_log.log', 'rb') as log_file:
            await bot.send_message(
                chat_id=admins_ids,
                text='Внимание! Случилась какая-то ошибка. Высылаю логги.\n\n'
                        'Логги высланы по вине следующей ошибки:\n\n' + str(exception)
            )

            await bot.send_document(
                chat_id=admins_ids,
                document=log_file
            )

    except FileNotFoundError as e:
        logger.error(f"send_logs_auto: logs file is not found {e}")

        # creating of logs file
        with open('main_log.log', "w"):
            pass

        logger.info(f"send_logs_auto: logs file created with the name 'main_log.log', because the upper Error {e}")

async def check_logs_size_and_delete(logs_file_path: str, max_size_bytes=1 * 1024 * 1024) -> None:
    """
    Проверяет размер файла логгов и, если размер больше максимального, удаляет его.

    :param logs_file_path: Путь, по которому, расположен файл логгов.
    :param max_size_bytes: Максимальный допустимый размер файла логгов. По умолчанию 1МБ в байтах.
    :return: None
    """

    try:
        file_size_bytes = os.path.getsize(logs_file_path)

        if file_size_bytes > max_size_bytes:
            os.remove(logs_file_path)
            logger.info(f"check_logs: The file {logs_file_path} deleted, "
                        f"because it's bigger than {max_size_bytes} in bytes.")

        else:
            logger.info(f"check_logs: Logs file's size checked. Nothing changed.")

    except (FileNotFoundError, PermissionError) as e:
        logger.error(f'check_logs: The file {logs_file_path} does not exist.')
        await send_logs_auto(e)

    except Exception as e:
        logger.error(f"check_logs {e}")
        await send_logs_auto(e)

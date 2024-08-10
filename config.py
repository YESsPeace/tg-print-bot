import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

import pickle

load_dotenv()

# настройка базового логгера
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (может быть DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
    filename='main_log.log',  # Имя файла, куда будут записываться логи
    filemode='a+',  # Режим записи (a - добавление, w - перезапись)
    encoding='utf-8'
)

logger = logging.getLogger(__name__)

admins_ids = (os.getenv('admins_ids')) # tuple[str]

# Глобальная переменная для уточнения цвета печати
try:
    with open("color_preset.pickle", "rb") as file:
        color_preset: bool = pickle.load(file) # True - colored, False - B&W
except:
    color_preset: bool = False # True - colored, False - B&W

storage = MemoryStorage()

bot = Bot(token=os.getenv('BOT_TOKEN')) # str
dp = Dispatcher(bot, storage=storage)
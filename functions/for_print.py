from PIL import Image
import io
import win32print
import win32ui
from PIL import ImageWin

from functions import send_logs_auto
from config import logger

async def print_image(image: bytes, colored: bool = False, orientation: str | None = None):
    img = Image.open(io.BytesIO(image))

    if not colored:
        img = img.convert('L')

    if (orientation == 'landscape') or ((orientation is None) and (img.height < img.width)):
        img = img.rotate(270, expand=True)

    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)

    try:
        # Начинаем документ печати
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc('Задача бота')
        hdc.StartPage()

        # Получите размеры страницы
        page_width = hdc.GetDeviceCaps(8)  # Ширина страницы
        page_height = hdc.GetDeviceCaps(10)  # Высота страницы

        # Вычисляем масштаб
        img_ratio = img.width / img.height
        page_ratio = page_width / page_height

        if img_ratio > page_ratio:
            # Изображение шире страницы
            new_width = page_width
            new_height = int(page_width / img_ratio)
        else:
            # Изображение выше страницы
            new_height = page_height
            new_width = int(page_height * img_ratio)

        # Изменяем размер изображения
        img = img.resize((new_width, new_height))

        # Вычисляем координаты для центрирования
        x_offset = (page_width - new_width) // 2
        y_offset = (page_height - new_height) // 2

        # Рисуем изображение с вычисленными смещениями
        dib = ImageWin.Dib(img)
        dib.draw(hdc.GetHandleOutput(), (x_offset, y_offset, x_offset + new_width, y_offset + new_height))

        # Завершаем страницу и документ
        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()
    
    except Exception as e:
        logger.error(f"print_image: {e}")
        await send_logs_auto(e)

    finally:
        win32print.ClosePrinter(hprinter)

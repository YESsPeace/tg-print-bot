from PIL import Image
import io
import win32print
import win32ui
from PIL import ImageWin

from functions.for_logs import send_logs_auto
from config import logger

async def print_image(image: bytes, colored: bool = False, orientation: str | None = None):
    img = Image.open(io.BytesIO(image))

    if not colored:
        img = img.convert('L')

    if orientation == 'landscape':
        img = img.rotate(270, expand=True)
    elif orientation == 'portrait':
        img = img.rotate(0, expand=True)

    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)

    try:
        # Начинаем документ печати
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc('Print Job')
        hdc.StartPage()

        # Печать изображения
        dib = ImageWin.Dib(img)
        dib.draw(hdc.GetHandleOutput(), (0, 0, img.size[0], img.size[1]))

        # Завершаем страницу и документ
        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()
    
    except Exception as e:
        logger.error(f"print_image: {e}")
        await send_logs_auto(e)

    finally:
        win32print.ClosePrinter(hprinter)

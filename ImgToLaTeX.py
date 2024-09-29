import os

try:
    from pix2tex.cli import LatexOCR
    from PIL import Image, ImageGrab

except:
    os.system("pip install pix2tex")
    os.system("pip install PIL")
    print("Execute again the script.")
    input(" ")
    exit(0)

import win32clipboard
import time

title_text = """
  _____              _______    _        _______  __   __
 |_   _|            |__   __|  | |      |__   __| \ \ / /
   | |  _ __ ___   __ _| | ___ | |     __ _| | ___ \ V / 
   | | | '_ ` _ \ / _` | |/ _ \| |    / _` | |/ _ \ > <  
  _| |_| | | | | | (_| | | (_) | |___| (_| | |  __// . \ 
 |_____|_| |_| |_|\__, |_|\___/|______\__,_|_|\___/_/ \_\
                   __/ |                                 
                  |___/                                  
"""

reset = '\033[0m'
bold = '\033[01m'
disable = '\033[02m'
underline = '\033[04m'
reverse = '\033[07m'
strikethrough = '\033[09m'
invisible = '\033[08m'


class fg:
    green = '\033[32m'
    cyan = '\033[36m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'


def get_clipboard_image():
    try:
        win32clipboard.OpenClipboard()
        data_available = win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_BITMAP)
        win32clipboard.CloseClipboard()

        if data_available:
            # ImageGrab.grabclipboard() devuelve la imagen del portapapeles si existe
            image = ImageGrab.grabclipboard()
            if image:
                return image
        return None

    except Exception as e:
        return None


def copy_to_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()


def send_title():
    print(fg.cyan + title_text + fg.green)
    print("Waiting for you to copy an image with a formula...  =)" + fg.lightblue)


def main():
    send_title()
    try:
        last_image = None
        while True:
            image = get_clipboard_image()
            if image and image != last_image:
                last_image = image
                print(fg.lightblue + "Detected a new image, processing with AI..." + fg.yellow)
                model = LatexOCR()

                latex_code = model(image)
                copy_to_clipboard(latex_code)
                print(fg.lightgreen + "LaTeX Copied to clipboard!")
                time.sleep(0.5)
    except KeyboardInterrupt:
        exit(0)


main()

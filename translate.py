from googletrans import Translator
import win32clipboard
from time import sleep
import keyboard
import pyautogui as pg
from infi.systray import SysTrayIcon


translate_button = "f8"
language = "en"

buttons = [f"f{i}" for i in range(1, 13)]


def show_help(systray):
    pg.alert(text=f'{translate_button} - Translate text\nYou can also change it', title='Help window', button='OK')


def change_translate_button(systray):
    global translate_button

    button = pg.prompt(text='Enter the new button(only f1-f12 avaible)', title='Set new button',
                       default=translate_button)
    translate_button_pre = translate_button

    if button in buttons:

        translate_button = button

        pg.alert(f"To save, click {translate_button_pre} first")


    else:
        pg.alert("Enter valid button!")


def exit(systray):
    import os
    os._exit(0)


def show_clipboard(systray):
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    language = translator.detect(data)

    pg.alert(f"Text: {data}\nLanguage: {language.lang}", "Clipboard text")


def change_language_en(systray):
    global language
    language = "en"


def change_language_ru(systray):
    global language
    language = "ru"


def change_language_az(systray):
    global language
    language = "az"


def translate_text():

    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        translate_text = str(translator.translate(data, dest=language).text)

        translate_text = translate_text.capitalize()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(translate_text, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
    except Exception as e:
        print(e)


translator = Translator()

menu_options = (('Help', None, show_help),
                ("Set new translate button", None, change_translate_button),
                ('Show clipboard text', None, show_clipboard),
                ('Change translate language', None, (('ru', "icons\\ru_icon.ico", change_language_ru),
                                                     ("en", "icons\\en_icon.ico", change_language_en),
                                                     ("az", "icons\\az_icon.ico", change_language_az),)
                 ),
                )
systray = SysTrayIcon("icons\\main_icon.ico", "TranslateApp", menu_options, on_quit=exit)
systray.start()

if __name__ == '__main__':
    while True:
        keyboard.wait(translate_button)
        translate_text()
        sleep(0.2)
        pg.hotkey('ctrl', 'v')




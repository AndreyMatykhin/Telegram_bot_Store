import os

from emoji import emojize

TOKEN = '7276103495:AAFa4Q63gJ1knSaSaz2UREUvlsyQl43jQns'
NAME_DB = 'products.sqlite'
VERSION = '0.0.1'
AUTHOR = 'Matyukhin_Andrey'

BASE_DIR = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], 'database')
os.makedirs(BASE_DIR, exist_ok=True)

DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_DB)
COUNT = 0

KEYBOARD = {
    'CHOOSE GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOUWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️'
}
CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
}

COMMANDS = {
    'START': "start",
    'HELP': "help",
}

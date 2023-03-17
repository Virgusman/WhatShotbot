from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon import LEXICON

#Инициализация кнопок:
button_1: KeyboardButton = KeyboardButton(text = LEXICON['play'])
button_2: KeyboardButton = KeyboardButton(text = LEXICON['faq'])
button_3: KeyboardButton = KeyboardButton(text = LEXICON['check'])

#Основная клавиатура на старте бота:
main_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2]], resize_keyboard=True)

#Основная клавиатура для роли модератора
admin_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2],[button_3]], resize_keyboard=True)
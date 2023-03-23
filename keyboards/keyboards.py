from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon import LEXICON

#Инициализация кнопок:
button_1: KeyboardButton = KeyboardButton(text = LEXICON['play_button'])
button_2: KeyboardButton = KeyboardButton(text = LEXICON['faq_button'])
button_3: KeyboardButton = KeyboardButton(text = LEXICON['check_button'])

#Основная клавиатура на старте бота:
main_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2]], resize_keyboard=True, one_time_keyboard=False)

#Основная клавиатура для роли модератора
admin_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2],[button_3]], resize_keyboard=True, one_time_keyboard=False)
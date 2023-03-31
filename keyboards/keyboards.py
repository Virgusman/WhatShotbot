from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon import LEXICON

#Инициализация кнопок:
button_1: KeyboardButton = KeyboardButton(text = LEXICON['play_button'])
button_2: KeyboardButton = KeyboardButton(text = LEXICON['faq_button'])
button_3: KeyboardButton = KeyboardButton(text = LEXICON['check_button'])
button_4: KeyboardButton = KeyboardButton(text = LEXICON['skip'])
button_5: KeyboardButton = KeyboardButton(text = LEXICON['rating'])

#Основная клавиатура на старте бота:
main_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2],[button_5]], resize_keyboard=True, one_time_keyboard=False)

#Основная клавиатура для роли модератора
admin_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1],[button_2],[button_5],[button_3]], resize_keyboard=True, one_time_keyboard=False)

#Клавиатура для пользователя В ИГРЕ
ingame_gb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_4],[button_2],[button_5]], resize_keyboard=True, one_time_keyboard=False)

#Клавиатура для админа в игре В ИГРЕ
adminingame_gb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_4],[button_2],[button_5],[button_3]], resize_keyboard=True, one_time_keyboard=False)
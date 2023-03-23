from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

#Админская клавиатура для проверки кадров
def create_editboard(id_shot: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['Shot_ok'],
                        callback_data= str(id_shot) + 'ok'),
                   InlineKeyboardButton(
                        text=LEXICON['Shot_Not_ok'],
                        callback_data= str(id_shot) + 'del'),
                   width=2)
    return kb_builder.as_markup()

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from lexicon.lexicon import LEXICON
from database import db

router: Router = Router()

#Нажатие на клавишу Проверить кадры
@router.message(Text(text=LEXICON['check_button']))
async def process_check(message: Message):
    if db.check_shot():
        print("есть новый кадр")
    else:
        print("новых кадров нет")




from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message
from lexicon.lexicon import LEXICON
from database import db
from keyboards.keyboards import main_kb,admin_kb


router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
@router.message(CommandStart())
async def process_start_command(message: Message):
    if not db.find_user(message.chat.id):
        db.add_user(message.from_user.id, message.from_user.full_name)
        await message.answer(text=LEXICON['hello first'], reply_markup=main_kb)
    else:
        await message.answer(text=message.from_user.full_name + LEXICON['hello again'], reply_markup=admin_kb if db.getAccess(message.from_user.id) else main_kb)


#Нажатие на клавишу Играть
@router.message(Text(text=LEXICON['play']))
async def process_play(message: Message):
    print("нажата кнопка")


#Нажатие на клавишу Справка
@router.message(Text(text=LEXICON['faq']))
async def process_faq(message: Message):
    pass

#Нажатие на клавишу Проверить кадры
@router.message(Text(text=LEXICON['check']))
async def process_check(message: Message):
    pass

@router.message(F.photo)
async def take_photo(message: Message):
    if message.caption == None:
        await message.answer(LEXICON['not_caption'])
    else:
        db.newShot(message.photo[-1].file_id, message.caption)
        await message.answer(LEXICON['addShot'])

#Ввод любого текста/ответа-названия фильма
@router.message(Text)
async def process(message: Message):
    pass
    
    








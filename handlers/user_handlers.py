
from aiogram import Router, F
from aiogram.filters import CommandStart, Text
from aiogram.types import Message
from lexicon.lexicon import LEXICON
from database import db
from keyboards.keyboards import main_kb, admin_kb, ingame_gb, adminingame_gb
from services.service import compare


router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
@router.message(CommandStart())
async def process_start_command(message: Message):
    if not db.find_user(message.chat.id):
        db.add_user(message.from_user.id, message.from_user.full_name)
        await message.answer(text=LEXICON['hello first'], reply_markup=main_kb)
    elif db.get_answer(message.from_user.id) != 0:
        await message.answer(text= message.from_user.full_name + LEXICON['hello in game'], 
                             reply_markup= adminingame_gb if db.getAccess(message.from_user.id) else ingame_gb)
    else:
        await message.answer(text=message.from_user.full_name + LEXICON['hello again'], 
                             reply_markup=admin_kb if db.getAccess(message.from_user.id) else main_kb)


#Нажатие на клавишу Играть
@router.message(Text(text=LEXICON['play_button']))
async def process_play(message: Message):
    shot = db.get_shot(message.from_user.id)
    if shot:
        await message.answer_photo(photo= shot[1],
                                        caption= LEXICON['caption_forgame'], 
                                        reply_markup= adminingame_gb if db.getAccess(message.from_user.id) else ingame_gb)
    else:
        await message.answer(LEXICON['Shot_notforgame'])


#Нажатие на клавишу Справка
@router.message(Text(text=LEXICON['faq_button']))
async def process_faq(message: Message):
    await message.answer(LEXICON['faq'])

#Нажатие на клавишу Пропустить кадр
@router.message(Text(text=LEXICON['skip']))
async def process_skip(message: Message):
    ans = db.get_answer(message.from_user.id)
    db.skip_shot(message.from_user.id)
    shot = db.get_shot(message.from_user.id)
    if shot:
        await message.answer_photo(photo= shot[1],
                                    caption= f"<b>Прошлый кадр был из фильма: {ans}</b>\n\n{LEXICON['caption_forgame']}", 
                                    reply_markup= adminingame_gb if db.getAccess(message.from_user.id) else ingame_gb)
    else:
        await message.answer(f"<b>Прошлый кадр был из фильма: {ans}</b>\n\n{LEXICON['Shot_notforgame']}", reply_markup=admin_kb if db.getAccess(message.from_user.id) else main_kb)

#Нажатие на клавишу Рейтинг
@router.message(Text(text=LEXICON['rating']))
async def process_rating(message: Message):
    points = db.get_top10()
    text : str = f"<b>🏅 Вами набрано: {str(db.get_points(message.from_user.id))} балла(ов)</b>\n\n"
    text += '<b>🏆 ТОП 10 игроков:</b>\n'
    for i in range(10):
        text += f"{str(i + 1)}. {points[i][0]}  - {str(points[i][1])} балла(ов)\n"
    await message.answer(text)





#Получение нового кадра от пользователя
@router.message(F.photo)
async def take_photo(message: Message):
    if message.caption == None:
        await message.answer(LEXICON['not_caption'])
    else:
        db.newShot(message.photo[-1].file_id, message.caption, message.from_user.id)
        await message.answer(LEXICON['addShot'])

#Ввод любого текста/ответа-названия фильма
@router.message(Text)
async def process_answer(message: Message):
    if db.get_answer(message.from_user.id) != 0:
        db.add_passed(message.from_user.id, message.text)    
        if compare(db.get_answer(message.from_user.id), message.text):
            db.win_shot(message.from_user.id)
            shot = db.get_shot(message.from_user.id)
            if shot:
                await message.answer_photo(photo= shot[1],
                                        caption= '✅ Правильно! Фильм отгадан!\n\n' + LEXICON['caption_forgame'], 
                                        reply_markup= adminingame_gb if db.getAccess(message.from_user.id) else ingame_gb)
            else:
                await message.answer('✅ Правильно! Фильм отгадан!\n\n' + LEXICON['Shot_notforgame'], reply_markup=admin_kb if db.getAccess(message.from_user.id) else main_kb)
        else:
            await message.answer('❌ Нет, ответ не верный. Попробуй еще или нажми "Пропустить кадр"')
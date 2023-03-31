from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON
from database import db
from keyboards.inline_keyboards import create_editboard

router: Router = Router()

#Нажатие на клавишу Проверить кадры
@router.message(Text(text=LEXICON['check_button']))
async def process_check(message: Message):
    if db.getAccess(message.from_user.id):
        photo = db.check_shot()
        if photo:
            await message.answer_photo(photo= photo[1],
                                        caption= "Название фильма: " + photo[2] + "\nДобавить данный кадр в игру или удалить?", 
                                        reply_markup= create_editboard(photo[0]))
        else:
            await message.answer('Новых кадров для проверки нет.')

#Нажатие на Инлайн-кнопку "Кадр в игру"
@router.callback_query(lambda x: 'ok' in x.data)
async def process_shot_ok(callback: CallbackQuery, bot: Bot):
    db.shot_ok(callback.message.chat.id, int(callback.data[:-2]))
    await callback.message.delete()
    photo = db.check_shot()
    if photo:
        await callback.message.answer_photo(photo= photo[1],
                                        caption= "Название фильма: " + photo[2] + "\nДобавить данный кадр в игру или удалить?", 
                                        reply_markup= create_editboard(photo[0]))
    else:
        users = db.get_users_notgame()
        for id in users:
            if id[0] != callback.message.chat.id:
                await bot.send_message(id[0], LEXICON['push_newshot'])
        await callback.message.answer('Новых кадров для проверки больше нет.')
    

#Нажатие на Инлайн-кнопку "Удалить кадр"
@router.callback_query(lambda x: 'del' in x.data)
async def process_shot_not_ok(callback: CallbackQuery, bot: Bot):
    db.shot_del(int(callback.data[:-3]))
    await callback.message.delete()
    photo = db.check_shot()
    if photo:
        await callback.message.answer_photo(photo= photo[1],
                                        caption= "Название фильма: " + photo[2] + "\nДобавить данный кадр в игру или удалить?", 
                                        reply_markup= create_editboard(photo[0]))
    else:
        users = db.get_users_notgame()
        for id in users:
            if id[0] != callback.message.chat.id:
                await bot.send_message(id[0], LEXICON['push_newshot'])
        await callback.message.answer('Новых кадров для проверки больше нет.')
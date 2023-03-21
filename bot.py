import asyncio

from aiogram import Bot, Dispatcher
from handlers import user_handlers
from config.config import TOKEN
from keyboards.main_menu import set_main_menu




# Функция конфигурирования и запуска бота
async def main():
     # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=TOKEN,parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    dp.include_router(user_handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    


if __name__ == '__main__':
    try:
        # Запускаем функцию main
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        print('Bot stopped!')

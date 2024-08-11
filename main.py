import asyncio
import logging


from aiogram import Bot, Dispatcher


from app.handlers.admin import admin
from app.handlers.user import user
from config import TOKEN


async def main():
    # await async_main()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(admin, user)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

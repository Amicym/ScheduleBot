import asyncio
import config
import logging
from app.handlers import rt 

from aiogram import Bot, Dispatcher, Router, F


bot = Bot(token=config.get_token())
dp = Dispatcher()

async def main():
    dp.include_router(rt)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
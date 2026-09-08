import asyncio
import config
import logging
from app.handlers import rt 
from curl_cffi.requests import AsyncSession

from aiogram import Bot, Dispatcher, Router, F


bot = Bot(token=config.get_token())
dp = Dispatcher()

async def main():
    dp.include_router(rt)

    session = AsyncSession(impersonate='chrome')
    dp.workflow_data["session"] = session

    try:
        await dp.start_polling(bot)
    finally:
        await session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
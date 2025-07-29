from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from src.handlers import repair_requests, menu, vehicles

from aiogram import Dispatcher


async def main():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties()
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(menu.router)
    dp.include_router(vehicles.router)
    dp.include_router(repair_requests.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
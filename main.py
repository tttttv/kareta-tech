from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers import repair_requests
from handlers import menu, vehicles


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
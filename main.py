from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handlers import repair_requests



from config import settings
from handlers import start, vehicles


async def main():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties()
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(vehicles.router)
    dp.include_router(repair_requests.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
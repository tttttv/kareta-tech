import base64

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

from src.config import settings
from src.handlers import repair_requests
from src.handlers import menu
from src.handlers import vehicles

from aiogram import Dispatcher


async def main():
    session = AiohttpSession()
    
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(),
        session=session
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(menu.router)
    dp.include_router(vehicles.router)
    dp.include_router(repair_requests.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

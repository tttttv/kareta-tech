from aiogram import Router, F, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from keyboards.inline import object_action_keyboard

from services.api_client import ApiClient


router = Router()


@router.message(Command("repair_requests"))
async def handle_repair_requests(message: types.Message):
    username = message.from_user.username
    api_client = ApiClient(username)


    requests = await api_client.get_vehicles()

    if not requests:
        await message.answer("🔧 У вас нет заявок на ремонт.")
        return

    for req in requests:
        text = (
            f"🪛 *Заявка #{req['id']}*\n"
            f"*ТС:* {req.vehicle['name']}\n"
            f"*Описание:* {req['description']}\n"
            f"*Статус:* {req['status']}\n"
            f"*Тип:* {req['request_type']}\n"
        )
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📄 Подробнее", callback_data=f"repair_req:{req['id']}")]
            ]
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=kb)


@router.callback_query(F.data.startswith("repair_req:"))
async def handle_repair_request_detail(callback: CallbackQuery):
    req_id = int(callback.data.split(":")[1])
    username = callback.from_user.username

    api_client = ApiClient(username)

    try:
        obj = await api_client.get_repair_requests(req_id)
        if obj:
            text = (
                f"🪛 *Заявка #{req_id['id']}*\n"
                f"*ТС:* {obj['name']}\n"
                f"*Описание:* {obj['description']}\n"
                f"*Статус:* {obj['status']}\n"
                f"*Тип:* {obj['request_type']}\n"
                f"*Автор:* {obj['author']}\n"
            )
            await callback.message.answer(text, reply_markup=object_action_keyboard(req_id))
        else:
            await callback.message.answer("Объект не найден.")

    finally:
        await api_client.close()

    await callback.answer()

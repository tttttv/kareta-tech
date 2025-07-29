from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from src.keyboards.inline import repair_request_action_keyboard
from src.services import repair_request
from contextlib import suppress

router = Router()


@router.callback_query(F.data.startswith("repair_req:"))
async def handle_repair_request_detail(callback: CallbackQuery):
    req_id = int(callback.data.split(":")[1])
    username = callback.from_user.username

    text = await repair_request.get_repair_request_by_id(username, req_id)

    if not text:
        text = "Объект не найден."

    kb = repair_request_action_keyboard(req_id)
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text, reply_markup=kb)

    await callback.answer()


@router.callback_query(F.data.startswith('set_repair_status'))
async def handle_set_repair_request_status(callback: types.CallbackQuery):
    "Изменить статус заявки"
    action, rep_id, status = callback.data.split(":")
    username = callback.from_user.username

    result = await repair_request.set_repair_status(username, rep_id, status)
    if result:
        await callback.message.edit_text("🚗 Статус обновлен.")

    updated_request = await repair_request.get_repair_request_by_id(username, rep_id)
    with suppress(TelegramBadRequest):
        kb = repair_request_action_keyboard(rep_id)
        await callback.message.edit_text(updated_request, reply_markup=kb)

    await callback.answer()



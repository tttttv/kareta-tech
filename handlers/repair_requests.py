from aiogram import Router, F, types
from aiogram.types import CallbackQuery

from keyboards.inline import repair_request_action_keyboard, repair_request_keyboard
from services import repair_request

router = Router()


@router.callback_query(F.data == "menu:requests")
async def menu_requests(callback: types.CallbackQuery):
    username = callback.from_user.username
    requests = await repair_request.get_repair_request(username)

    if not requests:
        await callback.message.edit_text("🔧 У вас нет заявок на ремонт.")
    else:
        await callback.message.edit_text("Выберите заявку:", reply_markup=repair_request_keyboard(requests))
    await callback.answer()


@router.callback_query(F.data.startswith("repair_req:"))
async def handle_repair_request_detail(callback: CallbackQuery):
    req_id = int(callback.data.split(":")[1])
    username = callback.from_user.username

    text = await repair_request.get_repair_request_by_id(username, req_id)

    if text:
        await callback.message.edit_text(text, reply_markup=repair_request_action_keyboard(req_id))
    else:
        await callback.message.edit_text("Объект не найден.")

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('set_repair_status'))
async def handle_set_status(callback: types.CallbackQuery):
    "Изменить статус заявки"
    action, rep_id, status = callback.data.split(":")
    username = callback.from_user.username

    result = await repair_request.set_repair_status(username, rep_id, status)
    if result:
        await callback.message.edit_text("🚗 Статус обновлен.")

    await callback.answer()


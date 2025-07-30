from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from src.keyboards.inline import repair_request_action_keyboard, vehicle_status_keyboard
from src.services import repair_request_service
from contextlib import suppress
from src.enums import VehicleRequestStatus, VehicleStatusEnum

router = Router()


@router.callback_query(F.data.startswith("repair_req:"))
async def handle_repair_request_detail(callback: CallbackQuery):
    req_id = int(callback.data.split(":")[1])
    username = callback.from_user.username

    obj = await repair_request_service.get_repair_request_by_id(username, req_id)
    text = obj.to_message()

    if not text:
        text = "Объект не найден."

    kb = repair_request_action_keyboard(obj.status, req_id)
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text, reply_markup=kb)

    await callback.answer()


@router.callback_query(F.data.startswith("set_repair_status:"))
async def handle_repair_status_change(callback: CallbackQuery):
    "Изменить статус заявки и передать в хэндлер для выбора статуса кареты"
    _, rep_id_str, request_status_str = callback.data.split(":")
    rep_id = int(rep_id_str)
    request_status = VehicleRequestStatus(request_status_str)
    username = callback.from_user.username

    if request_status == VehicleRequestStatus.IN_PROGRESS:
        # Показываем клавиатуру с выбором нового статуса для кареты
        await callback.message.edit_text(
            "Выберите новый статус кареты:",
            reply_markup=vehicle_status_keyboard(rep_id, request_status)
        )
    elif request_status == VehicleRequestStatus.COMPLETED:
        # Отправляем сразу оба новых статуса
        await repair_request_service.update_request_and_vehicle_status(
            username,
            request_id=rep_id,
            request_status=request_status,
            vehicle_status=VehicleStatusEnum.AVAILABLE
        )

        await callback.message.edit_text(
            "Статусы обновлены ✅",
            reply_markup=repair_request_action_keyboard(request_status, rep_id)
        )


@router.callback_query(F.data.startswith("set_vehicle_status:"))
async def handle_vehicle_status_selection(callback: CallbackQuery):
    "Изменить статус кареты"
    _, rep_id_str, request_status_str, vehicle_status_str = callback.data.split(":")
    rep_id = int(rep_id_str)
    request_status = VehicleRequestStatus(request_status_str)
    vehicle_status = VehicleStatusEnum(vehicle_status_str)
    username = callback.from_user.username

    await repair_request_service.update_request_and_vehicle_status(
        username,
        request_id=rep_id,
        request_status=request_status,
        vehicle_status=vehicle_status
    )

    await callback.message.edit_text(
        "Статусы обновлены 🛠",
        reply_markup=repair_request_action_keyboard(request_status, rep_id)
    )
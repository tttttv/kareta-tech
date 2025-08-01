from aiogram import Router, F, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

from src.keyboards.inline import repair_request_action_keyboard, vehicle_status_keyboard, \
    repair_request_keyboard, after_repair_status_change_action_keyboard
from src.services import repair_request_service
from contextlib import suppress
from src.enums import VehicleRequestStatus, VehicleStatusEnum
from src.keyboards.utils.nav_keyboard import MENU_BUTTON, BACK_TO_REPAIR_REQUESTS
from aiogram.fsm.context import FSMContext

router = Router()


@router.callback_query(F.data.startswith("repair_req:"))
async def handle_repair_request_detail(callback: CallbackQuery):
    "Получить заявку по ее айди"

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
    current_request_status = VehicleRequestStatus(request_status_str)
    username = callback.from_user.username

    if current_request_status == VehicleRequestStatus.IN_PROGRESS:

        await callback.message.edit_text(
            "Выберите новый статус кареты:",
            reply_markup=vehicle_status_keyboard(rep_id, current_request_status)
        )
    elif current_request_status == VehicleRequestStatus.COMPLETED or current_request_status == VehicleRequestStatus.WAITING:
        # Отправляем сразу оба новых статуса
        await repair_request_service.update_request_and_vehicle_status(
            username,
            request_id=rep_id,
            request_status=current_request_status,
            vehicle_status=VehicleStatusEnum.AVAILABLE
        )
        return_status = VehicleRequestStatus.IN_PROGRESS
        await callback.message.edit_text(
            "Статусы обновлены ✅",
            reply_markup=after_repair_status_change_action_keyboard(return_status, rep_id)
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
    # Меняем статус на противоположный чтобы по кнопке назад вернуться обратно к заявкам в данном статусе
    if request_status == VehicleRequestStatus.IN_PROGRESS or VehicleRequestStatus.WAITING:
        return_status = VehicleRequestStatus.COMPLETED
    else:
        return_status = VehicleRequestStatus.IN_PROGRESS

    await callback.message.edit_text(
        "Статусы обновлены 🛠",
        reply_markup=after_repair_status_change_action_keyboard(return_status, rep_id)
    )


@router.callback_query(F.data.startswith("requests_by_geo:"))
async def show_requests_by_geozone(callback_query: types.CallbackQuery, state: FSMContext):
    "Показать заявки на ремонт по геозоне"

    request_type = callback_query.data.split(":")[1]
    username = callback_query.from_user.username
    data = await state.get_data()
    geozone_id = data.get("geozone_id")

    repair_requests = await repair_request_service.get_requests_by_geozone(username, geozone_id)

    if not repair_requests:
        await callback_query.message.edit_text(
            "Заявок не найдено.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[BACK_TO_REPAIR_REQUESTS] + [MENU_BUTTON]
            )
        )
        return

    if request_type == "active":
        requests = [
            r for r in repair_requests
            if r.status in [VehicleRequestStatus.WAITING, VehicleRequestStatus.IN_PROGRESS]
        ]
    else:
        requests = [
            r for r in repair_requests
            if r.status == VehicleRequestStatus.COMPLETED
        ]

    if not requests:
        await callback_query.message.edit_text(
            "Заявок не найдено.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[BACK_TO_REPAIR_REQUESTS] + [MENU_BUTTON])
        )
        return

    await callback_query.message.edit_text(
        f"Список заявок ({'активных' if request_type == 'active' else 'завершённых'}):",
        reply_markup=repair_request_keyboard(requests)
    )
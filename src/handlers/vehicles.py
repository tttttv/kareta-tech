from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.keyboards.inline import vehicle_action_keyboard
from src.services import vehicles
from src.keyboards.utils.nav_keyboard import append_navigation_keyboard
from aiogram.types import LinkPreviewOptions
from contextlib import suppress

router = Router()


@router.callback_query(F.data.startswith("vehicle:"))
async def handle_vehicle_selection(callback: types.CallbackQuery):
    "Получить карету по ее айди"

    vehicle_id = callback.data.split(":")[1]
    username = callback.from_user.username

    result = await vehicles.get_vehicle_by_id(username, vehicle_id)

    if result:
        await callback.message.edit_text(result)
    else:
        await callback.message.edit_text("Объект не найден.")

    kb = vehicle_action_keyboard(vehicle_id)
    kb_with_nav = append_navigation_keyboard(kb)

    await callback.message.edit_text(result, reply_markup=kb_with_nav)

    await callback.answer()


@router.callback_query(F.data.startswith(("lock:", "unlock:", "beep:")))
async def handle_vehicle_actions(callback: types.CallbackQuery):
    action, vehicle_id = callback.data.split(":")
    username = callback.from_user.username

    if action == "lock":
        await vehicles.lock_vehicle(username, vehicle_id)
        text = "🚗 Карета заблокирована."
    elif action == "unlock":
        await vehicles.unlock_vehicle(username, vehicle_id)
        text = "🚗 Карета разблокирована."
    elif action == "beep":
        await vehicles.beep(username, vehicle_id)
        text ="Сигнал отправлен."
    else:
        text = 'Неизвестная команда.'

    kb = vehicle_action_keyboard(vehicle_id)
    kb_with_nav = append_navigation_keyboard(kb)

    await callback.message.edit_text(text, reply_markup=kb_with_nav)
    await callback.answer()


@router.callback_query(F.data.startswith('set_status'))
async def handle_set_vehicle_status(callback: types.CallbackQuery):
    "Изменить статус"
    action, vehicle_id, status = callback.data.split(":")

    username = callback.from_user.username

    result = await vehicles.set_status(username, vehicle_id, status)
    if result:
        await callback.message.edit_text("🚗 Статус обновлен.")

    updated_vehicle =await vehicles.get_vehicle_by_id(username, vehicle_id)
    with suppress(TelegramBadRequest):
        kb = vehicle_action_keyboard(vehicle_id)
        kb_with_nav = append_navigation_keyboard(kb)
        await callback.message.edit_text(updated_vehicle, reply_markup=kb_with_nav)

    await callback.answer()


@router.callback_query(F.data.startswith('location'))
async def handle_vehicle_location(callback: types.CallbackQuery):
    "Изменить статус"
    _, vehicle_id = callback.data.split(":")

    username = callback.from_user.username

    location_url = await vehicles.get_vehicle_location(username, vehicle_id)
    # Создаем кнопку с URL
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺 Открыть в браузере", url=location_url)]
    ])

    # Отправляем сообщение с кнопкой
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы открыть местоположение:",
        reply_markup=kb,
        link_preview_options=LinkPreviewOptions(
            url=location_url,
            prefer_small_media=True
        )
    )

    kb = vehicle_action_keyboard(vehicle_id)
    kb_with_nav = append_navigation_keyboard(kb)
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=kb_with_nav
    )

    await callback.answer()


@router.callback_query(F.data.startswith("vehicle_by_request:"))
async def handle_vehicle_by_request(callback: types.CallbackQuery):
    "Получить карету по ее айди"

    request_id = callback.data.split(":")[1]
    username = callback.from_user.username

    result = await vehicles.get_vehicle_by_request_id(username, request_id)

    if result:
        await callback.message.edit_text(result.to_message())
    else:
        await callback.message.edit_text("Объект не найден.")

    kb = vehicle_action_keyboard(result.id)
    kb_with_nav = append_navigation_keyboard(kb)

    await callback.message.edit_text(result.to_message(), reply_markup=kb_with_nav)

    await callback.answer()


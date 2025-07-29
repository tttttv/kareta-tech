from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.keyboards.inline import vehicle_action_keyboard
from src.services import vehicles
from src.keyboards.inline import main_menu_keyboard
from aiogram.types import LinkPreviewOptions
from contextlib import suppress
from aiogram.fsm.context import FSMContext
from src.states.states import SearchVehicleStates

router = Router()


@router.callback_query(F.data.startswith("vehicle:"))
async def handle_vehicle_selection(callback: types.CallbackQuery):
    "Получить карету по ее айди"

    vehicle_id = callback.data.split(":")[1]
    username = callback.from_user.username

    result = await vehicles.get_vehicle_by_id(username, vehicle_id)

    if result:
        kb = vehicle_action_keyboard(vehicle_id, result.is_locked)
        await callback.message.edit_text(
            result.to_message(),
            reply_markup=kb
        )
    else:
        await callback.message.edit_text(
            "Объект не найден.",
            reply_markup=main_menu_keyboard()
        )

    await callback.answer()


@router.callback_query(F.data.startswith(("lock:", "unlock:", "beep:")))
async def handle_vehicle_actions(callback: types.CallbackQuery):
    action, vehicle_id = callback.data.split(":")
    username = callback.from_user.username

    is_locked = False
    if action == "lock":
        vehicle =await vehicles.lock_vehicle(username, vehicle_id)
        is_locked = True
        text = "🚗 Карета заблокирована."
    elif action == "unlock":
        vehicle = await vehicles.unlock_vehicle(username, vehicle_id)
        text = "🚗 Карета разблокирована."
    elif action == "beep":
        vehicle = await vehicles.beep(username, vehicle_id)
        text ="Сигнал отправлен."
    else:
        vehicle = None
        text = 'Неизвестная команда.'
    with suppress(TelegramBadRequest):
        kb = vehicle_action_keyboard(vehicle_id, is_locked)
        answer = text + "\n\n" + vehicle.to_message() if vehicle else text
        await callback.message.edit_text(answer, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith('set_status'))
async def handle_set_vehicle_status(callback: types.CallbackQuery):
    "Изменить статус"
    action, vehicle_id, status = callback.data.split(":")

    username = callback.from_user.username

    result = await vehicles.set_status(username, vehicle_id, status)
    if result:
        await callback.message.edit_text("🚗 Статус обновлен.")

    updated_vehicle = await vehicles.get_vehicle_by_id(username, vehicle_id)
    with suppress(TelegramBadRequest):
        kb = vehicle_action_keyboard(vehicle_id, result.is_locked)
        await callback.message.edit_text(updated_vehicle.to_message(), reply_markup=kb)

    await callback.answer()


@router.callback_query(F.data.startswith('location'))
async def handle_vehicle_location(callback: types.CallbackQuery):
    "Изменить статус"
    _, vehicle_id = callback.data.split(":")

    username = callback.from_user.username

    location_url, vehicle = await vehicles.get_vehicle_with_location(username, vehicle_id)
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

    kb = vehicle_action_keyboard(vehicle_id, vehicle.is_locked)
    await callback.message.answer(
        "Выберите действие:",
        reply_markup=kb
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

    kb = vehicle_action_keyboard(result.id, result.is_locked)

    await callback.message.edit_text(result.to_message(), reply_markup=kb)

    await callback.answer()


@router.callback_query(F.data == "find_vehicle")
async def ask_for_vehicle_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ID кареты:")
    await state.set_state(SearchVehicleStates.waiting_for_vehicle_id)
    await callback.answer()


@router.message(SearchVehicleStates.waiting_for_vehicle_id)
async def process_vehicle_id_input(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, введите число.")
        return

    username = message.from_user.username

    vehicle_id = int(message.text)
    await state.clear()

    vehicle_info = await vehicles.get_vehicle_by_id(username, vehicle_id)

    if vehicle_info:
        kb = vehicle_action_keyboard(vehicle_id, vehicle_info.is_locked)
        await message.answer(
            f"🚗 Карета найдена:\n{vehicle_info.to_message()}",
            reply_markup=kb
        )
    else:
        await message.answer(
            "❌ Карета с таким ID не найдена.",
            reply_markup=main_menu_keyboard())
import asyncio

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import LinkPreviewOptions

from src.keyboards.inline import main_menu_keyboard
from src.keyboards.inline import vehicle_action_keyboard
from src.services import vehicles_service
from src.states.states import SearchVehicleStates
from src.utils.animation import show_loading_animation

router = Router()


@router.callback_query(F.data.startswith("vehicle:"))
async def handle_vehicle_selection(callback: types.CallbackQuery):
    "Получить карету по ее айди"

    vehicle_id = callback.data.split(":")[1]
    username = callback.from_user.username

    result = await vehicles_service.get_vehicle_by_id(username, vehicle_id)

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
async def handle_vehicle_action(callback: types.CallbackQuery):
    action, vehicle_id = callback.data.split(":")
    vehicle_id = int(vehicle_id)
    username = callback.from_user.username

    msg = await callback.message.edit_text("🕐 Выполняется команда...", reply_markup=None)
    animation_task = asyncio.create_task(show_loading_animation(msg, f"Выполняется {action.upper()}"))

    await callback.message.edit_text(
        f"⏳ Выполняется команда {action.upper()}...",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⏳", callback_data="wait")]])
    )
    if action == "lock":
        vehicle = await vehicles_service.lock_vehicle_with_waiting(username,vehicle_id)
        text = f"🔒 Карета {vehicle.name} заблокирована"
    elif action == "unlock":
        vehicle = await vehicles_service.unlock_vehicle_with_waiting(username, vehicle_id)
        text = f"🔓 Карета {vehicle.name} разблокирована"
    elif action == "beep":
        vehicle = await vehicles_service.beep(username, vehicle_id)
        text ="Сигнал отправлен."
    else:
        vehicle = None
        text = 'Неизвестная команда.'

    await callback.message.edit_text(
        text + "\n\n" + vehicle.to_message() if vehicle else text,
        reply_markup=vehicle_action_keyboard(vehicle_id, is_locked=vehicle.is_locked)
    )
    animation_task.cancel()


@router.callback_query(F.data.startswith('location'))
async def handle_vehicle_location(callback: types.CallbackQuery):
    "Изменить статус"
    _, vehicle_id = callback.data.split(":")

    username = callback.from_user.username

    location_url, vehicle = await vehicles_service.get_vehicle_with_location(username, vehicle_id)
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

    result = await vehicles_service.get_vehicle_by_request_id(username, request_id)

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

    vehicle_info = await vehicles_service.get_vehicle_by_id(username, vehicle_id)

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
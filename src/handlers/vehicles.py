# import asyncio

from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import LinkPreviewOptions

from src.keyboards.inline import main_menu_keyboard
from src.keyboards.inline import vehicle_action_keyboard
from src.services import vehicles_service
from src.states.states import SearchVehicleStates
# from src.utils.animation import show_loading_animation
from src.constants import MANUAL_LOCK_PROTOCOLS
from src.utils.command_name_builder import get_true_command_name


router = Router()

@router.callback_query(F.data.startswith("vehicle:"))
async def handle_vehicle_selection(
    callback: types.CallbackQuery
):
    """Получить карету по ее айди"""

    vehicle_id = callback.data.split(":")[1]
    username = callback.from_user.username

    result = await vehicles_service.get_vehicle_by_id(
        username=username, 
        vehicle_id=vehicle_id
    )

    actual_vehicle_command = await vehicles_service.get_actual_vehicle_command_status(
        username=username, 
        vehicle_id=vehicle_id
    )
    
    if result:
        kb = vehicle_action_keyboard(
            vehicle_id=vehicle_id, 
            is_locked=result.is_locked,
            is_manual_lock=True if result.lock_type in MANUAL_LOCK_PROTOCOLS else False,
            actual_command=actual_vehicle_command.command_name
        )
        
        try:
            await callback.message.edit_text(
                text=result.to_message(),
                reply_markup=kb
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                # Просто игнорируем эту ошибку
                await callback.answer()
            else:
                raise
        
        # await callback.message.edit_text(
        #     result.to_message(),
        #     reply_markup=kb
        # )
    else:
        await callback.message.edit_text(
            "Объект не найден.",
            reply_markup=main_menu_keyboard()
        )

    await callback.answer()

@router.callback_query(
    F.data.startswith(
        (
            "lock:", 
            "unlock:", 
            "beep:", 
            "set_tracking_interval_30:",
            "set_tracking_interval_60:", 
            "update_vehicle_location:"
        )
    )
)
async def handle_vehicle_action(
    callback: types.CallbackQuery
):
    action, vehicle_id = callback.data.split(":")
    vehicle_id = int(vehicle_id)
    username = callback.from_user.username

    # msg = await callback.message.edit_text(
    #     "🕐 Выполняется команда...", 
    #     reply_markup=None
    # )
    
    # command = await vehicles_service.get_actual_vehicle_command_status(
    #     username=username, 
    #     vehicle_id=vehicle_id
    # )
    
    # kb_buttons = [
    #     [
    #         InlineKeyboardButton(
    #             text="⏳", 
    #             callback_data="wait"
    #         )
    #     ],
    # ]
    
    vehicle = await vehicles_service.get_vehicle_by_id(
        username=username, 
        vehicle_id=vehicle_id
    )
    
    true_command_name = get_true_command_name(command_name=action, vehicle_type=vehicle.lock_type)

    kb_buttons = [
        [
            InlineKeyboardButton(
                text="Отменить", 
                callback_data=f"cancel_command:{vehicle_id}:{true_command_name}"
            )
        ]
    ]

    await callback.message.edit_text(
        f"⏳ Выполняется команда {action.upper()}...",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                *kb_buttons
            ]
        )
    )
    
    if action == "lock":
        vehicle = await vehicles_service.lock_vehicle_with_waiting(
            username=username,
            vehicle_id=vehicle_id
        )
        if vehicle:
            text = f"🔒 Карета {vehicle.name} заблокирована"
    elif action == "unlock":
        vehicle = await vehicles_service.unlock_vehicle_with_waiting(
            username=username, 
            vehicle_id=vehicle_id
        )
        if vehicle:
            text = f"🔓 Карета {vehicle.name} разблокирована"
    elif action == "beep":
        vehicle = await vehicles_service.beep(
            username=username, 
            vehicle_id=vehicle_id
        )
        text ="Сигнал отправлен."
    elif action == "set_tracking_interval_30":
        vehicle = await vehicles_service.set_tracking_interval_30(
            username=username, 
            vehicle_id=vehicle_id
        )
        text = "Новый интервал отслеживания установлен."
    elif action == "set_tracking_interval_60":
        vehicle = await vehicles_service.set_tracking_interval_60(
            username=username, 
            vehicle_id=vehicle_id
        )
        text = "Новый интервал отслеживания установлен."
    elif action == "update_vehicle_location":
        vehicle = await vehicles_service.force_get_location(
            username=username, 
            vehicle_id=vehicle_id
        )
        text = "Координаты обновлены"
    else:
        vehicle = None
        text = 'Неизвестная команда.'

    if not vehicle:
        text = "Ошибка при выполнении команды."
        vehicle = await vehicles_service.get_vehicle_by_id(
            username=username, 
            vehicle_id=vehicle_id
        )
    
    await callback.message.edit_text(
        text + "\n\n" + vehicle.to_message() if vehicle else text,
        reply_markup=vehicle_action_keyboard(
            vehicle_id=vehicle_id, 
            is_locked=vehicle.is_locked
        )
    )
    # animation_task.cancel()

@router.callback_query(F.data.startswith('location'))
async def handle_vehicle_location(
    callback: types.CallbackQuery
):
    """Изменить статус"""
    
    _, vehicle_id = callback.data.split(":")

    username = callback.from_user.username

    location_url, vehicle = await vehicles_service.get_vehicle_with_location(
        username=username, 
        vehicle_id=vehicle_id
    )
    
    # NOTE: Создаем кнопку с URL
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗺 Открыть в браузере", 
                    url=location_url
                )
            ]
        ]
    )

    # NOTE: Отправляем сообщение с кнопкой
    await callback.message.answer(
        "Нажмите кнопку ниже, чтобы открыть местоположение:",
        reply_markup=kb,
        link_preview_options=LinkPreviewOptions(
            url=location_url,
            prefer_small_media=True
        )
    )

    kb = vehicle_action_keyboard(
        vehicle_id=vehicle_id, 
        is_locked=vehicle.is_locked
    )
    await callback.message.answer(
        "Выберите действие:",
        reply_markup=kb
    )

    await callback.answer()

@router.callback_query(F.data.startswith("vehicle_by_request:"))
async def handle_vehicle_by_request(
    callback: types.CallbackQuery
):
    """Получить карету по ее айди"""

    request_id = callback.data.split(":")[1]
    username = callback.from_user.username

    result = await vehicles_service.get_vehicle_by_request_id(
        username=username, 
        request_id=request_id
    )

    if result:
        await callback.message.edit_text(result.to_message())
    else:
        await callback.message.edit_text("Объект не найден.")

    kb = vehicle_action_keyboard(result.id, result.is_locked)

    await callback.message.edit_text(
        result.to_message(), 
        reply_markup=kb
    )

    await callback.answer()

@router.callback_query(F.data == "find_vehicle")
async def ask_for_vehicle_code(
    callback: types.CallbackQuery, 
    state: FSMContext
):
    """Предложение ввести код кареты для поиска"""
    
    await callback.message.answer("Введите название (код) кареты:")
    await state.set_state(SearchVehicleStates.waiting_for_vehicle_id)
    await callback.answer()

@router.message(SearchVehicleStates.waiting_for_vehicle_id)
async def process_vehicle_code_input(
    message: types.Message, 
    state: FSMContext
):
    """Обработка ввода кода кареты"""
    
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, введите число.")
        return

    username = message.from_user.username
    # vehicle_id = int(message.text)
    vehicle_code = message.text

    await state.clear()

    # vehicle_info = await vehicles_service.get_vehicle_by_id(
    #     username=username, 
    #     vehicle_id=vehicle_id
    # )

    vehicle_info = await vehicles_service.get_vehicle_by_code(
        username=username, 
        vehicle_code=vehicle_code
    )
    
    actual_vehicle_command = await vehicles_service.get_actual_vehicle_command_status(
        username=username, 
        vehicle_id=vehicle_info.id
    )

    if vehicle_info == "not found":
        await message.answer(
            "❌ Карета по данному коду не найдена.",
            reply_markup=main_menu_keyboard()
        )
    elif vehicle_info == "forbidden":
        await message.answer(
            "❌ Карета по данному коду Вам недоступна.",
            reply_markup=main_menu_keyboard()
        )
    else:
        kb = vehicle_action_keyboard(
            vehicle_id=vehicle_info.id, 
            is_locked=vehicle_info.is_locked,
            is_manual_lock=True if vehicle_info.lock_type in MANUAL_LOCK_PROTOCOLS else False,
            actual_command=actual_vehicle_command.command_name
        )
        await message.answer(
            f"🚗 Карета найдена:\n{vehicle_info.to_message()}",
            reply_markup=kb
        )

@router.callback_query(F.data.startswith('cancel_command:'))
async def handle_cancel_command(
    callback: types.CallbackQuery
):
    vehicle_id = callback.data.split(":")[1]
    command_name = callback.data.split(":")[2]
    
    username = callback.from_user.username

    command_canceling_result = await vehicles_service.cancel_command(
        username=username, 
        vehicle_id=vehicle_id, 
        command_name=command_name
    )

    if command_canceling_result:
        await callback.answer("Команда успешно отменена.")
    else:
        await callback.answer("Команда не может быть отменена.")
    
    result = await vehicles_service.get_vehicle_by_id(
        username=username, 
        vehicle_id=vehicle_id
    )

    actual_vehicle_command = await vehicles_service.get_actual_vehicle_command_status(
        username=username, 
        vehicle_id=vehicle_id
    )
    
    if result:
        kb = vehicle_action_keyboard(
            vehicle_id=vehicle_id, 
            is_locked=result.is_locked,
            is_manual_lock=True if result.lock_type in MANUAL_LOCK_PROTOCOLS else False,
            actual_command=actual_vehicle_command.command_name
        )
        
        try:
            await callback.message.edit_text(
                text=result.to_message(),
                reply_markup=kb
            )
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                # Просто игнорируем эту ошибку
                await callback.answer()
            else:
                raise
        
        # await callback.message.edit_text(
        #     result.to_message(),
        #     reply_markup=kb
        # )
    else:
        await callback.message.edit_text(
            "Объект не найден.",
            reply_markup=main_menu_keyboard()
        )

    await callback.answer()

from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.keyboards.inline import vehicle_keyboard
from src.keyboards.inline import request_type_keyboard
from src.keyboards.inline import geozone_selecting_keyboard
from src.keyboards.inline import start_keyboard
from src.keyboards.inline import main_menu_keyboard
from src.keyboards.inline import geozone_objects_kb
from src.services import main_menu_service
from src.services import vehicles_service
from src.services.api_client import ApiClient


router = Router()

@router.message(CommandStart())
async def send_welcome(
    message: types.Message
):
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=start_keyboard()
    )

@router.message(F.text == 'start')
@router.message(Command("start"))
async def start_menu(
    message: types.Message
):
    """Главное меню"""

    username = message.from_user.username
    chat_id = message.chat.id
    async with ApiClient(username) as client:
        result = await client.register_chat_id(chat_id)
    if result:

        await message.answer("Выберите действие:", reply_markup=main_menu_keyboard())
    else:
        await message.answer("Вы не зарегистрированы в системе. Свяжитесь с администратором.")


@router.callback_query(F.data == "choose_geozone")
async def choose_geozone(
    callback: types.CallbackQuery, 
    state: FSMContext
):
    """Выбрать геозону"""

    username = callback.from_user.username
    geozones = await main_menu_service.get_user_geozones(username)

    if not geozones:
        await callback.message.answer("Нет доступных геозон.")
        return

    await callback.message.edit_text(
        "Выберите геозону:",
        reply_markup=geozone_selecting_keyboard(geozones)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("geozone:"))
async def handle_geozone_objects_selection(
    callback: types.CallbackQuery, 
    state: FSMContext
):
    """Выбрать объекты геозоны"""

    geozone_id = callback.data.split(":")[1]
    if geozone_id:
        await state.update_data(geozone_id=geozone_id)

    await callback.message.edit_text(
        "Выберите действие:", 
        reply_markup=geozone_objects_kb()
    )
    
    await callback.answer()


@router.callback_query(F.data == "to_start")
async def return_to_start_menu(
    callback: types.CallbackQuery
):
    """Вернуться в главное меню"""

    await callback.message.edit_text(
        "Выберите, что хотите сделать:",
        reply_markup=main_menu_keyboard()
    )


@router.callback_query(F.data == "menu:vehicles_by_geozone")
async def menu_vehicles_by_geozone(
    callback: types.CallbackQuery, 
    state: FSMContext
):
    "Показать меню выбора кареты"

    data = await state.get_data()
    geozone_id = data.get("geozone_id")
    
    if not geozone_id:
        await callback.message.edit_text(
            "Выберите, что хотите сделать:",
            reply_markup=main_menu_keyboard()
        )
    
    username = callback.from_user.username

    objects = await vehicles_service.get_vehicles_by_geozone(
        username=username, 
        geozone_id=geozone_id
    )

    if objects:
        await callback.message.edit_text(
            "Выберите карету:", 
            reply_markup=vehicle_keyboard(objects)
        )
    else:
        await callback.message.edit_text(
            "В этой геозоне нет доступных карет.", 
            reply_markup=main_menu_keyboard()
        )

    await callback.answer()


@router.callback_query(F.data == "menu:requests_by_geozone")
async def requests_menu_by_geozone(
    callback_query: types.CallbackQuery, 
    state: FSMContext
):
    "Показать меню выбора типа заявок на ремонт"

    data = await state.get_data()
    geozone_id = data.get("geozone_id")

    if not geozone_id:
        await callback_query.message.edit_text(
            "Сначала выберите геозону.",
            reply_markup=main_menu_keyboard()
        )
        return

    # Показываем меню выбора типа заявок
    await callback_query.message.edit_text(
        "Выберите тип заявок:",
        reply_markup=request_type_keyboard()
    )

from aiogram import Router, types, F
from aiogram.filters import Command
from src.keyboards.inline import main_menu_keyboard
from src.services import repair_request_service, vehicles_service
from src.keyboards.inline import vehicle_keyboard, repair_request_keyboard, request_type_keyboard
from src.services.api_client import ApiClient


router = Router()


@router.message(F.text == 'start')
@router.message(Command("start"))
async def start_menu(message: types.Message):
    username = message.from_user.username
    chat_id = message.chat.id
    async with ApiClient(username) as client:
        result = await client.register_chat_id(chat_id)
    if result:
        await message.answer(
            "Выберите, что хотите сделать:",
            reply_markup=main_menu_keyboard()
        )
    else:
        await message.answer("Вы не зарегистрированы в системе. Свяжитесь с администратором.")


@router.callback_query(F.data == "to_start")
async def return_to_start_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите, что хотите сделать:",
        reply_markup=main_menu_keyboard()
    )


@router.callback_query(F.data == "menu:vehicles")
async def menu_vehicles(callback: types.CallbackQuery):
    username = callback.from_user.username
    objects = await vehicles_service.get_vehicles(username)

    if objects:
        await callback.message.edit_text("Выберите карету:", reply_markup=vehicle_keyboard(objects))
    else:
        await callback.message.edit_text(
            "У вас нет доступных карет.",
            reply_markup=main_menu_keyboard()
        )
    await callback.answer()


@router.callback_query(F.data == "menu:requests")
async def requests_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите тип заявок:",
        reply_markup=request_type_keyboard()
    )
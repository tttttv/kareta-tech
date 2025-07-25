from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.inline import main_menu_keyboard
from services import vehicles, repair_request
from keyboards.inline import vehicle_keyboard, repair_request_keyboard

router = Router()


@router.message(Command("start"))
async def start_menu(message: types.Message):
    await message.answer(
        "Выберите, что хотите сделать:",
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "menu:vehicles")
async def menu_vehicles(callback: types.CallbackQuery):
    username = callback.from_user.username
    objects = await vehicles.get_vehicles(username)
    if objects:
        await callback.message.edit_text("Выберите карету:", reply_markup=vehicle_keyboard(objects))
    else:
        await callback.message.edit_text("У вас нет доступных карет.")


@router.callback_query(F.data == "menu:requests")
async def menu_requests(callback: types.CallbackQuery):
    username = callback.from_user.username
    objects = await repair_request.get_repair_request(username)
    if objects:
        await callback.message.edit_text("Выберите заявку:", reply_markup=repair_request_keyboard(objects))
    else:
        await callback.message.edit_text("У вас нет открытых заявок.")
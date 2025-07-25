from aiogram import Router, types, F
from services.api_client import ApiClient
from keyboards.inline import vehicle_action_keyboard
from keyboards.inline import vehicle_keyboard
from services import vehicles, repair_request
from keyboards.utils.nav_keyboard import append_navigation_keyboard

router = Router()


@router.callback_query(F.data == "menu:vehicles")
async def menu_vehicles(callback: types.CallbackQuery):
    username = callback.from_user.username
    objects = await vehicles.get_vehicles(username)

    if objects:
        await callback.message.edit_text("Выберите карету:", reply_markup=vehicle_keyboard(objects))
    else:
        await callback.message.edit_text("У вас нет доступных карет.")
    await callback.edit_text()


@router.callback_query(lambda c: c.data.startswith("select:"))
async def handle_vehicle_selection(callback: types.CallbackQuery):
    "Получить карету по ее айди"

    vehicle_id = callback.data.split(":")[1]
    username = callback.from_user.username

    result = await vehicles.get_vehicle_by_id(username, vehicle_id)

    if result:
        await callback.message.edit_text(result, reply_markup=vehicle_action_keyboard(vehicle_id))
    else:
        await callback.message.edit_text("Объект не найден.")

    await callback.edit_text()


@router.callback_query(lambda c: c.data.startswith(("lock:", "unlock:", "beep:")))
async def handle_vehicle_actions(callback: types.CallbackQuery):
    action, vehicle_id = callback.data.split(":")
    username = callback.from_user.username

    if action == "lock":
        await vehicles.lock_vehicle(username, vehicle_id)
        await callback.message.edit_text("🚗 Карета заблокирована.")
    elif action == "unlock":
        await vehicles.unlock_vehicle(username, vehicle_id)
        await callback.message.edit_text("🚗 Карета разблокирована.")
    elif action == "delete":
        await vehicles.beep(username, vehicle_id)
        await callback.message.edit_text("🗑 Карета удалена.")

    await callback.edit_text()


@router.callback_query(lambda c: c.data.startswith('set_status'))
async def handle_set_status(callback: types.CallbackQuery):
    "Изменить статус"
    action, vehicle_id, status = callback.data.split(":")
    username = callback.from_user.username

    result = await repair_request.set_repair_status(username, vehicle_id, status)
    if result:
        await callback.message.edit_text("🚗 Статус обновлен.")

    await callback.edit_text()



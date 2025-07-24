from aiogram import Router, types
from services.api_client import ApiClient
from keyboards.inline import object_action_keyboard
from keyboards.inline import objects_keyboard

router = Router()


@router.message()
async def send_vehicle_list(message: types.Message):
    "Получить список карет"

    username = message.from_user.username
    api_client = ApiClient(username)

    objects = await api_client.get_vehicles()
    if objects:
        await message.answer("Выберите карету:", reply_markup=objects_keyboard(objects))
    else:
        await message.answer("У вас нет доступных карет.")


@router.callback_query(lambda c: c.data.startswith("select:"))
async def handle_vehicle_selection(callback: types.CallbackQuery):
    "Получить карету по ее айди"

    vehicle_id = callback.data.split(":")[1]
    username = callback.from_user.username

    api_client = ApiClient(username)

    try:
        obj = await api_client.get_vehicle_by_id(vehicle_id)

        if obj:
            text = (
                f"Имя: {obj['name']}\n"
                f"Цвет: {obj['color']}\n"
                f"Пробег: {obj['mileage']}\n"
                f"Вне геозоны: {obj['is_left_geozone']}\n"
                f"Модель: {obj['model']['name']}\n"
                f"Число мест: {obj['model']['seating_capacity']}\n"
                f"IMEI: {obj['imei']}\n"
                f"Статус: {obj['status']}\n"
                f"Статус замка: {obj['is_locked']}\n"
                f"Геозона: {obj['geozone']['name']}\n"
                f"[📍 Открыть на карте]({obj['location_link']})"
            )
            await callback.message.answer(text, reply_markup=object_action_keyboard(vehicle_id))
        else:
            await callback.message.answer("Объект не найден.")

    finally:
        await api_client.close()

    await callback.answer()


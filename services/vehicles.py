from services.api_client import ApiClient



async def get_vehicles(username):
    "Получить список карет"

    async with ApiClient(username) as client:
        return await client.get_vehicles()


async def get_vehicle_by_id(username, vehicle_id):
    "Получить карету по ее айди"


    async with ApiClient(username) as client:
        obj = await client.get_vehicle_by_id(vehicle_id)

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
            return text
        return None

async def lock_vehicle(username, vehicle_id):
    "Заблокировать карету"
    async with ApiClient(username) as client:
        await client.lock_vehicle(vehicle_id)
    return True

async def unlock_vehicle(username, vehicle_id):
    "Разблокировать карету"
    async with ApiClient(username) as client:
        await client.unlock_vehicle(vehicle_id)
    return True

async def beep(username, vehicle_id):
    "Подать звуковой сигнал"
    async with ApiClient(username) as client:
        await client.beep_vehicle(vehicle_id)
    return True

from src.services.api_client import ApiClient
from src.schemas.vehicle_schemas import VehicleSchema


async def get_vehicles(username):
    "Получить список карет"

    async with ApiClient(username) as client:
        return await client.get_vehicles()


async def get_vehicle_by_id(username, vehicle_id):
    "Получить карету по ее айди"

    async with ApiClient(username) as client:
        obj = await client.get_vehicle_by_id(vehicle_id)
        if obj:
            vehicle = VehicleSchema(**obj)

            return vehicle.to_message()
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

async def set_status(username, vehicle_id, status):
    async with ApiClient(username) as client:
        await client.set_vehicle_status(vehicle_id, status)


async def get_vehicle_by_request_id(username, request_id):
    async with ApiClient(username) as client:
        obj = await client.get_vehicle_by_request_id(request_id)

        if obj:
            return VehicleSchema(**obj)

        return None


async def get_vehicle_location(username, vehicle_id):
    async with ApiClient(username) as client:
        vehicle = await client.get_vehicle_by_id(vehicle_id)
        location = vehicle['last_location']

        longitude = location['lon']
        latitude = location['lat']
        zoom = 16
        url = f"https://yandex.ru/maps/?ll={longitude},{latitude}&pt={longitude},{latitude}&z={zoom}"
        return url

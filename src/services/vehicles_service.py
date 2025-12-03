import asyncio

from src.services.api_client import ApiClient
from src.schemas.vehicle_schemas import VehicleSchema
from src.schemas.vehicle_schemas import VehicleLockShema


async def get_vehicles(
    username
):
    """Получить список карет"""

    async with ApiClient(username) as client:
        return await client.get_vehicles()

async def get_vehicles_by_geozone(
    username, 
    geozone_id
):
    """Получить список карет в геозоне"""

    async with ApiClient(username) as client:
        result = await client.get_geozone_vehicles(geozone_id)
        return result

async def get_vehicle_by_id(
    username, 
    vehicle_id
):
    """Получить карету по ее айди"""

    async with ApiClient(username) as client:
        obj = await client.get_vehicle_by_id(vehicle_id)
        if obj:
            try:
                return VehicleSchema(**obj)
            except Exception:
                return obj

        return None

async def lock_vehicle_with_waiting(
    username, 
    vehicle_id
):
    """Заблокировать карету с ожиданием"""
    
    async with ApiClient(username) as client:
        for _ in range(60):
            result = await client.lock_vehicle(vehicle_id)
            if result:
                try:
                    VehicleLockShema(**result)
                except:
                    try:
                        return VehicleSchema(**result)
                    except:
                        return
            await asyncio.sleep(1)

async def lock_vehicle(
    username, 
    vehicle_id
):
    """Заблокировать карету"""
    
    async with ApiClient(username) as client:
        result = await client.lock_vehicle(vehicle_id)
    return VehicleSchema(**result)

async def unlock_vehicle(
    username, 
    vehicle_id
):
    """Разблокировать карету"""
    
    async with ApiClient(username) as client:
        result = await client.unlock_vehicle(vehicle_id)
    return VehicleSchema(**result)

async def unlock_vehicle_with_waiting(
    username, 
    vehicle_id
):
    """Заблокировать карету с ожиданием"""
    
    async with ApiClient(username) as client:
        for _ in range(60):
            result = await client.unlock_vehicle(vehicle_id)
            if result:
                try:
                    VehicleLockShema(**result)
                except:
                    try:
                        return VehicleSchema(**result)
                    except:
                        return
            await asyncio.sleep(1)

async def beep(
    username, 
    vehicle_id
) -> VehicleSchema:
    """Подать звуковой сигнал"""
    
    async with ApiClient(username) as client:
        result =await client.beep_vehicle(vehicle_id)
        
    return VehicleSchema(**result)

async def set_tracking_interval_30(
    username, 
    vehicle_id
) -> VehicleSchema:
    """Установить интервал отслеживания 30 секунд"""
    
    async with ApiClient(username) as client:
        result = await client.set_tracking_interval_30(vehicle_id)
        
    return VehicleSchema(**result)

async def set_tracking_interval_60(
    username, 
    vehicle_id
) -> VehicleSchema:
    """Установить интервал отслеживания 60 секунд"""
    
    async with ApiClient(username) as client:
        result = await client.set_tracking_interval_60(vehicle_id)
        
    return VehicleSchema(**result
)

async def force_get_location(
    username, 
    vehicle_id
) -> VehicleSchema:
    """Принудительно получить координаты"""
    
    async with ApiClient(username) as client:
        result = await client.force_get_location(vehicle_id)
        
    return VehicleSchema(**result
)

async def set_status(
    username, 
    vehicle_id, 
    status
) -> VehicleSchema:
    """Изменить статус ТС"""
    
    async with ApiClient(username) as client:
        result = await client.set_vehicle_status(
            vehicle_id=vehicle_id, 
            status=status
        )
        res_schema = VehicleSchema(**result)
        return res_schema

async def get_vehicle_by_request_id(
    username, 
    request_id
):
    """Получить карету по айди заявки на ремонт"""
    
    async with ApiClient(username) as client:
        obj = await client.get_vehicle_by_request_id(request_id)

        if obj:
            try:
                return VehicleSchema(**obj)
            except Exception:
                return obj

        return None

async def get_vehicle_with_location(
    username, 
    vehicle_id
):
    """Получить карету с координатами"""
    
    async with ApiClient(username) as client:
        vehicle_request = await client.get_vehicle_by_id(vehicle_id)
        vehicle = VehicleSchema(**vehicle_request)
        location = vehicle.last_location

        longitude = location['lon']
        latitude = location['lat']
        zoom = 16
        url = f"https://yandex.ru/maps/?ll={longitude},{latitude}&pt={longitude},{latitude}&z={zoom}"
        return url, vehicle

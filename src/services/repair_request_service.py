from src.services.api_client import ApiClient
from src.schemas.repair_request_schemas import RepairRequestSchema
from src.schemas.vehicle_schemas import VehicleSchema


async def get_repair_request(username):
    async with ApiClient(username) as client:
        result = await client.get_repair_requests()
        return [RepairRequestSchema(**r) for r in result]

async def get_repair_request_by_id(
    username, 
    req_id
):
    async with ApiClient(username) as client:
        req = await client.get_repair_request_by_id(req_id)

        if not req:
            return

        req_model = RepairRequestSchema(**req)

        return req_model

async def set_repair_status(
    username, 
    repair_id, 
    status
):
    async with ApiClient(username) as client:
        await client.set_repair_status(repair_id, status)

    return True

async def update_request_and_vehicle_status(
    username,
    request_id,
    request_status,
    vehicle_status
):
    async with ApiClient(username) as client:
        return await client.update_request_and_vehicle_status(
            request_id,
            request_status,
            vehicle_status
        )
        
async def update_vehicle_status(
    username,
    vehicle_id,
    vehicle_status
) -> VehicleSchema:
    async with ApiClient(username) as client:
        result = await client.set_vehicle_status(
            vehicle_id=vehicle_id, 
            status=vehicle_status
        )
        
        return VehicleSchema(**result)

async def get_requests_by_geozone(username, geozone_id):
    async with ApiClient(username) as client:
        resutl = await client.get_geozone_requests(geozone_id)
        return [RepairRequestSchema(**r) for r in resutl]

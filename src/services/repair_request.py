from src.services.api_client import ApiClient
from src.schemas.repair_request_schemas import RepairRequestSchema


async def get_repair_request(username):
    async with ApiClient(username) as client:
        return await client.get_repair_requests()


async def get_repair_request_by_id(username, req_id):
    async with ApiClient(username) as client:
        req = await client.get_repair_request_by_id(req_id)

        if not req:
            return

        req_model = RepairRequestSchema(**req)

        return req_model.to_message()

async def set_repair_status(username, repair_id, status):
    async with ApiClient(username) as client:
        await client.set_repair_status(repair_id, status)

    return True

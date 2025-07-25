from services.api_client import ApiClient


async def get_repair_request(username):
    async with ApiClient(username) as client:
        return await client.get_repair_requests()


async def get_repair_request_by_id(username, req_id):
    async with ApiClient(username) as client:
        req = await client.get_repair_request_by_id(req_id)

        if not req:
            return

        text = (
            f"🪛 *Заявка #{req['id']}*\n"
            f"*ТС:* {req['vehicle']['name']}\n"
            f"*Описание:* {req['description']}\n"
            f"*Статус:* {req['status']}\n"
            f"*Тип:* {req['request_type']}\n"
        )

        return text

async def set_repair_status(username, repair_id, status):
    async with ApiClient(username) as client:
        await client.set_repair_status(repair_id, status)

    return True

import aiohttp
from config import settings


class ApiClient:
    def __init__(self, username):
        self.base_url = settings.api_base_url
        self.username_payload = {'username': username}
        self.session = None

    async def initialize(self):
        self.session = aiohttp.ClientSession(headers={'x-tg-secret': f'{settings.secret}'})

    async def close(self):
        if self.session:
            await self.session.close()

    async def request(self, method, path, *, data=None, params=None):
        if self.session is None:
            await self.initialize()

        url = f"{self.base_url}{path}"
        try:
            async with self.session.request(method, url, json=data, params=params, ssl=False) as response:
                response.raise_for_status()
                if response.content_type == 'application/json':
                    return await response.json()
                return await response.text()
        finally:
            await self.close()

    async def get_vehicles(self):
        return await self.request("POST", '/', data=self.username_payload)

    async def get_vehicle_by_id(self, vehicle_id):
        path = f'/{vehicle_id}'

        return await self.request("POST", path, data=self.username_payload)

    async def lock_vehicle(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/lock'
        return await self.request("PUT", path, data=self.username_payload)

    async def unlock_vehicle(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/unlock'
        return await self.request("PUT", path, data=self.username_payload)

    async def beep_vehicle(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/beep'
        return await self.request("POST", path, data=self.username_payload)

    async def set_vehicle_status(self, vehicle_id, status):
        path = f'/vehicles/{vehicle_id}/status'
        data = {"status": status, **self.username_payload}  # todo
        return await self.request("PATCH", path, data=data)

    async def get_repair_requests(self):
        path = f'/repair-requests'
        return await self.request("POST", path, data=self.username_payload)

    async def get_repair_request_by_id(self, req_id):
        path = f'/repair-requests/{req_id}'
        return await self.request("POST", path, data=self.username_payload)

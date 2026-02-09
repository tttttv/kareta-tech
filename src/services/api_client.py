import aiohttp
from src.config import settings
import backoff
from aiohttp import ClientResponseError


class ApiClient:
    def __init__(self, username):
        self.base_url = settings.api_base_url
        self.username = username
        self.session = None

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def initialize(self):
        self.session = aiohttp.ClientSession(
            headers={
                'x-tg-secret': f'{settings.secret}',
                'x-tg-username': f'{self.username}'
            }
        )

    async def close(self):
        if self.session:
            await self.session.close()

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_time=5)
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
        except ClientResponseError as e:
            if e.status == 403:
                return {"error": "forbidden"}
            elif e.status == 404:
                return {"error": "not found"}
            else:
                raise

    async def get_vehicles(self):
        return await self.request("GET", '/vehicles')

    async def get_vehicle_by_id(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}'
        response = await self.request("GET", path)
        if "error" in response:
            return response['error']

        return response

    async def get_vehicle_by_code(self, vehicle_code):
        path = f'/vehicles/get_by_code/{vehicle_code}'
        response = await self.request("GET", path)
        
        if "error" in response:
            return response['error']
        
        return response
    
    async def get_vehicle_by_request_id(self, request_id):
        path = f'/repair-requests/{request_id}/vehicle'

        return await self.request("GET", path)

    async def lock_vehicle(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/lock'
        return await self.request("POST", path)

    async def unlock_vehicle(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/unlock'
        return await self.request("POST", path)

    async def beep_vehicle(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/beep'
        return await self.request("POST", path)

    async def set_tracking_interval_30(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/tracking-interval-30'
        return await self.request("POST", path)

    async def set_tracking_interval_60(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/tracking-interval-60'
        return await self.request("POST", path)
    
    async def force_get_location(self, vehicle_id):
        path = f'/vehicles/{vehicle_id}/force-get-location'
        return await self.request("POST", path)
    
    async def set_vehicle_status(self, vehicle_id, status):
        path = f'/vehicles/{vehicle_id}/status/{status}'
        return await self.request("POST", path)

    async def get_repair_requests(self):
        path = f'/repair-requests'
        return await self.request("GET", path)

    async def get_repair_request_by_id(self, req_id):
        path = f'/repair-requests/{req_id}'
        return await self.request("GET", path)

    async def set_repair_status(self, request_id, status):
        path = f'/repair-requests/status/{request_id}'
        return await self.request("POST", path, data={"status": status})

    async def update_request_and_vehicle_status(self, request_id, request_status, vehicle_status):
        path = f'/repair-requests/vehicle-request-status/{request_id}'
        updated_vehicle = await self.request(
            "PUT",
            path,
            data={"vehicle_status": vehicle_status, "repair_status": request_status}
        )
        return updated_vehicle

    async def register_chat_id(self, chat_id):
        path = f'/register_chat_id'
        return await self.request("POST", path, data={"chat_id": chat_id})

    async def get_geozones(self):
        path = f'/allowed-geozones'
        return await self.request("GET", path)

    async def get_geozone_vehicles(self, geozone_id):
        path = f'/geozones/{geozone_id}/vehicles'
        return await self.request("GET", path)

    async def get_geozone_requests(self, geozone_id):
        path = f'/geozones/{geozone_id}/repair-requests'
        return await self.request("GET", path)

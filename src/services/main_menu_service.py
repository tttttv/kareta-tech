from src.services.api_client import ApiClient
from src.schemas.geozone_schema import GeozoneSchema


async def get_user_geozones(username):
    async with ApiClient(username) as client:
        result = await client.get_geozones()
        return [GeozoneSchema(**g) for g in result]

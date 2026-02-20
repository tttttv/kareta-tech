from pydantic import BaseModel


class GeozoneSchema(BaseModel):
    id: int
    name: str

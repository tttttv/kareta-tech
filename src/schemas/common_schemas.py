from pydantic import BaseModel
from pydantic import Field


class BooleanResponseSchema(BaseModel):
    result: bool = Field(..., description="Результат")

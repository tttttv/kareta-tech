from pydantic import BaseModel
from src.schemas.vehicle_schemas import VehicleShortSchema



class RepairRequestSchema(BaseModel):
    id: int
    status: str
    vehicle: VehicleShortSchema
    status: str
    request_type: str
    description: str
    is_active: bool

    def to_message(self):
        text = (
            f"🪛 *Заявка #{self.id}*\n"
            f"*ТС:* {self.vehicle.name}\n"
            f"*Описание:* {self.description}\n"
            f"*Статус:* {self.status}\n"
            f"*Тип:* {self.request_type}\n"
            f"*Активный:* {self.is_active}\n"
            f"*Айди кареты:* {self.vehicle.id}\n"
            f"*Название кареты:* {self.vehicle.name}\n"

        )
        return text

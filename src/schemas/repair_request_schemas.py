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

    def to_message(self) -> str:
        text = (
            f"🛠 Заявка #{self.id}\n\n"
            f"📌 Основная информация\n"
            f"- Статус: {'✅' if self.status == 'COMPLETED' else '🕓'} {self.status}\n"
            f"- Тип: 🔧 {self.request_type}\n\n"
            f"🛺 Объект\n"
            f"- Название кареты: {self.vehicle.name}\n"
            f"- ID кареты: #{self.vehicle.id}\n"
            f"- Активный: {'✔️ True (Активна)' if self.is_active else '❌ False (Неактивна)'}\n\n"
            f"📝 Описание работ\n"
            f"{self.description}"
        )
        return text

from pydantic import BaseModel
from pydantic import Field


class VehicleModelSchema(BaseModel):
    name: str
    brand: str
    # seating_capacity: str


class GeoZoneSchema(BaseModel):
    name: str


class VehicleLockShema(BaseModel):
    status: str
    detail: str


class VehicleSchema(BaseModel):
    id: int
    name: str
    status: str
    color: str
    lock_type: str
    mileage: float
    is_left_geozone: bool
    model: VehicleModelSchema | None
    imei: int
    status: str
    is_locked: bool
    geozone: GeoZoneSchema | None
    last_location: dict
    is_active: bool

    def to_message(self) -> str:
        text = (
            "🛺  Объект\n\n"
            f"- Имя: {self.name}\n"
            f"- Модель: {self.model.name if self.model else ''}\n"
            # f"- Число мест: {self.model.seating_capacity if self.model else ''}\n"
            f"- Цвет: ⬛️ {self.color}\n"
            f"- Идентификатор (ID): {self.id}\n\n"

            "📊 Показатели\n"
            f"- Пробег: {self.mileage} км\n"
            f"- Статус: {'✅ ' + self.status if self.status else ''}\n"
            f"- Активный: {'✔️ True' if self.is_active else '❌ False'}\n\n"

            "🔒 Замок\n"
            f"- Статус замка: {'🔒 Закрыт' if self.is_locked else '🔓 Открыт'}\n"
            f"- Тип замка: {self.lock_type}\n"
            f"- IMEI: {self.imei}\n\n"

            "🌍 Геоданные\n"
            f"- Геозона: {self.geozone.name if self.geozone else ''}\n"
            f"- Вне геозоны: {'❌ False' if not self.is_left_geozone else '⚠️ True'}"
        )
        return text


class VehicleShortSchema(BaseModel):
    id: int
    name: str
    color: str


class VehicleCommandStatusSchema(BaseModel):
    status: bool = Field(..., description="Статус команды")
    command_name: str | None = Field(default=None, description="Название команды")

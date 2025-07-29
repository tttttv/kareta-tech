from pydantic import BaseModel


class VehicleModelSchema(BaseModel):
    name: str
    brand: str
    seating_capacity: str


class GeoZoneSchema(BaseModel):
    name: str


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
            f"Имя: {self.name}\n"
            f"Цвет: {self.color}\n"
            f"Пробег: {self.mileage}\n"
            f"Вне геозоны: {self.is_left_geozone}\n"
            f"Модель: {self.model.name}\n"
            f"Число мест: {self.model.seating_capacity if self.model else ''}\n"
            f"IMEI: {self.imei}\n"
            f"Статус: {self.status}\n"
            f"Статус замка: {self.is_locked}\n"
            f"Тип замка: {self.lock_type}\n"
            f"Геозона: {self.geozone.name if self.geozone else ''}\n"
            f"Активный: {self.is_active}\n"
        )
        return text


class VehicleShortSchema(BaseModel):
    id: int
    name: str
    color: str


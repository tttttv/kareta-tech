from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton

from src.enums import VehicleRequestStatus
from src.enums import VehicleStatusEnum
from src.keyboards.utils.nav_keyboard import (
    MENU_BUTTON, 
    BACK_TO_GEOZONES, 
    BACK_TO_REPAIR_REQUESTS, 
    BACK_TO_GEOZONE_SELECTION
)
from src.schemas.geozone_schema import GeozoneSchema


def vehicle_keyboard(objects):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=obj['name'], callback_data=f"vehicle:{obj['id']}")]
            for obj in objects
        ] + [BACK_TO_GEOZONES] +[MENU_BUTTON]
    )
    return kb

def vehicle_action_keyboard(
    vehicle_id: int, 
    is_locked: bool,
    is_manual_lock: bool = False
) -> InlineKeyboardMarkup:
    
    lock_button = None
    
    if is_locked:
        lock_button = InlineKeyboardButton(text="🔓 Открыть", callback_data=f"unlock:{vehicle_id}")
    else:
        if not is_manual_lock:
            lock_button = InlineKeyboardButton(text="🔒 Закрыть", callback_data=f"lock:{vehicle_id}")
        
    
    # lock_button = (
    #     InlineKeyboardButton(text="🔓 Открыть", callback_data=f"unlock:{vehicle_id}")
    #     if is_locked
    #     else InlineKeyboardButton(text="🔒 Закрыть", callback_data=f"lock:{vehicle_id}")
    # )

    map_keyboard_button = InlineKeyboardButton(text="🗺️ На карте", callback_data=f"location:{vehicle_id}")
    first_row = []
    
    if lock_button:
        first_row.append(lock_button)

    first_row.append(map_keyboard_button)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            first_row,
            [
                InlineKeyboardButton(text="📣 Сигнал", callback_data=f"beep:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="🔨 Изменить статус", callback_data=f"get_keyboard_to_set_vehicle_status:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="🔃 Интервал отправки координат 30 сек.", callback_data=f"set_tracking_interval_30:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="🔃 Интервал отправки координат 60 сек.", callback_data=f"set_tracking_interval_60:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="🧭 Обновить текущие координаты", callback_data=f"update_vehicle_location:{vehicle_id}")
                # TODO: Нужно разобраться с тем, что у нас по перезагрузке замка (на одном из протоколов её нет)
            ]
        ] + [
            [
                InlineKeyboardButton(text="Назад", callback_data="menu:vehicles_by_geozone")
            ]
        ] + [
            MENU_BUTTON
        ]
    )
    
    return kb

def repair_request_keyboard(objects):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Звявка №{obj.id}', callback_data=f"repair_req:{obj.id}")]
            for obj in objects
        ] + [BACK_TO_REPAIR_REQUESTS] + [MENU_BUTTON]
    )
    return kb

def repair_request_action_keyboard(request_status, rep_id) -> InlineKeyboardMarkup:
    buttons = []

    if request_status == VehicleRequestStatus.IN_PROGRESS:
        buttons.append(
            InlineKeyboardButton(
                text="✅ Завершен",
                callback_data=f"set_repair_status:{rep_id}:{VehicleRequestStatus.COMPLETED.value}"
            )
        )
    else:
        buttons.append(
            InlineKeyboardButton(
                text="🛠 В ремонт",
                callback_data=f"set_repair_status:{rep_id}:{VehicleRequestStatus.IN_PROGRESS.value}"
            )
        )

    buttons_markup = [[button] for button in buttons]
    buttons_markup.append([
        InlineKeyboardButton(text="К карете", callback_data=f"vehicle_by_request:{rep_id}")
    ])

    if request_status in (VehicleRequestStatus.IN_PROGRESS, VehicleRequestStatus.WAITING):
        return_status = 'active'
    else:
        return_status = 'completed'

    buttons_markup.append([InlineKeyboardButton(text="Назад", callback_data=f"requests_by_geo:{return_status}")])
    buttons_markup.append(MENU_BUTTON)

    return InlineKeyboardMarkup(inline_keyboard=buttons_markup)

def vehicle_status_keyboard_without_request(
    vehicle_id: int,
) -> InlineKeyboardMarkup:
    statuses = [
        (VehicleStatusEnum.UNAVAILABLE_IN_SERVICE, "🔧 Ремонт"),
        (VehicleStatusEnum.UNAVAILABLE_IN_SERVICE, "🩸 Донор"),
        (VehicleStatusEnum.UNAVAILABLE_IN_MAINTENANCE, "🛠 Обслуживание"),
        (VehicleStatusEnum.AVAILABLE, "🚚 Доступна"),
    ]
    buttons = [
        InlineKeyboardButton(
            text=label,
            callback_data=f"set_vehicle_status_without_request:{vehicle_id}:{veh_status.value}"
        ) for veh_status, label in statuses
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons] + [MENU_BUTTON])

def vehicle_status_keyboard(rep_id: int, request_status: VehicleRequestStatus) -> InlineKeyboardMarkup:
    statuses = [
        (VehicleStatusEnum.UNAVAILABLE_IN_SERVICE, "🔧 Ремонт"),
        (VehicleStatusEnum.UNAVAILABLE_IN_SERVICE, "🩸 Донор"),
        (VehicleStatusEnum.UNAVAILABLE_IN_MAINTENANCE, "🛠 Обслуживание"),
        (VehicleStatusEnum.AVAILABLE, "🚚 Доступна"),
    ]
    buttons = [
        InlineKeyboardButton(
            text=label,
            callback_data=f"set_vehicle_status:{rep_id}:{request_status.value}:{veh_status.value}"
        ) for veh_status, label in statuses
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons] + [MENU_BUTTON])

def geozone_objects_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Кареты", callback_data="menu:vehicles_by_geozone"),
            InlineKeyboardButton(text="🔧 Заявки", callback_data="menu:requests_by_geozone"),
        ],
        BACK_TO_GEOZONE_SELECTION,
        MENU_BUTTON
    ])
    return kb

def main_menu_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📍 Выбрать геозону", callback_data="choose_geozone"),
            InlineKeyboardButton(text="Найти по айди", callback_data="find_vehicle"),
        ]
    ])
    return kb

def geozone_selecting_keyboard(geozones: list[GeozoneSchema]) -> InlineKeyboardMarkup:
     kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=g.name, callback_data=f"geozone:{g.id}")]
            for g in geozones
        ] + [MENU_BUTTON]
    )
     return kb

def request_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Активные", callback_data=f"requests_by_geo:active"),
                InlineKeyboardButton(text="☑️ Завершённые", callback_data=f"requests_by_geo:completed"),
            ]
        ] + [BACK_TO_GEOZONES] + [MENU_BUTTON]
    )

def start_keyboard():
    return ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="start")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

def after_repair_status_change_action_keyboard(request_status, rep_id) -> InlineKeyboardMarkup:
    buttons = []

    buttons_markup = [[button] for button in buttons]
    buttons_markup.append([
        InlineKeyboardButton(text="К карете", callback_data=f"vehicle_by_request:{rep_id}")
    ])

    if request_status in (VehicleRequestStatus.IN_PROGRESS, VehicleRequestStatus.WAITING):
        return_status = 'active'
    else:
        return_status = 'completed'

    buttons_markup.append([InlineKeyboardButton(text="Назад", callback_data=f"requests_by_geo:{return_status}")])
    buttons_markup.append(MENU_BUTTON)

    return InlineKeyboardMarkup(inline_keyboard=buttons_markup)

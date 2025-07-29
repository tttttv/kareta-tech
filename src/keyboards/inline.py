from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from enums import VehicleRequestStatus
from enums import VehicleStatusEnum


def vehicle_keyboard(objects):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=obj['name'], callback_data=f"vehicle:{obj['id']}")]
            for obj in objects
        ]
    )
    return kb


def vehicle_action_keyboard(vehicle_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔒 Заблокировать", callback_data=f"lock:{vehicle_id}"),
                InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"unlock:{vehicle_id}"),
                InlineKeyboardButton(text='Посмотреть на карте', callback_data=f"location:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="📣 Сигнал", callback_data=f"beep:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="✅ Доступен", callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.AVAILABLE.value}"),
                InlineKeyboardButton(text="🚫 Ремонт", callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.UNAVAILABLE_IN_SERVICE.value}")
            ],
            [
                InlineKeyboardButton(text="🚫 Донор", callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.UNAVAILABLE_DONOR.value}"),
                InlineKeyboardButton(text="🚫 Обслуж.", callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.UNAVAILABLE_IN_MAINTENANCE.value}")
            ]
        ]
    )
    return kb


def repair_request_keyboard(objects):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Звявка №{obj["id"]}', callback_data=f"repair_req:{obj['id']}")]
            for obj in objects
        ]
    )
    return kb



def repair_request_action_keyboard(rep_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=
            [
                [InlineKeyboardButton(text="🛠 В ремонт", callback_data=f"set_repair_status:{rep_id}:{VehicleRequestStatus.IN_PROGRESS.value}")],
                [InlineKeyboardButton(text="✅ Завершен", callback_data=f"set_repair_status:{rep_id}:{VehicleRequestStatus.COMPLETED.value}")],
                [InlineKeyboardButton(text="К карете", callback_data=f"vehicle_by_request:{rep_id}")],
        ]
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Кареты", callback_data="menu:vehicles"),
            InlineKeyboardButton(text="🔧 Заявки", callback_data="menu:requests"),
        ]
    ])
    return kb

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from enums import VehicleRequestStatus
from enums import VehicleStatusEnum


def vehicle_keyboard(objects):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=obj['name'], callback_data=f"select:{obj['id']}")]
            for obj in objects
        ]
    )
    return kb


def vehicle_action_keyboard(vehicle_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔒 Заблокировать", callback_data=f"lock:{vehicle_id}"),
                InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"unlock:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="📣 Подать сигнал", callback_data=f"beep:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="✅ Доступен", callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.AVAILABLE}"),
                InlineKeyboardButton(text="🚫 Недоступен, ремонт", callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.UNAVAILABLE_IN_SERVICE}"),
                InlineKeyboardButton(text="🚫 Недоступен, донор", callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.UNAVAILABLE_DONOR}"),
                InlineKeyboardButton(text="🚫 Недоступен, обслуживание",  callback_data=f"set_status:{vehicle_id}:{VehicleStatusEnum.UNAVAILABLE_IN_MAINTENANCE}"),
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
                [InlineKeyboardButton(text="🛠 В ремонт", callback_data=f"set_repair_status:{rep_id}:{VehicleRequestStatus.IN_PROGRESS}")],
                [InlineKeyboardButton(text="✅ Завершен", callback_data=f"set_repair_status:{rep_id}:{VehicleRequestStatus.COMPLETED}")],
                [],
                [InlineKeyboardButton(text="🚘 Список доступных карет", callback_data="menu:vehicles")],
                [InlineKeyboardButton(text="🛠 Заявки на обслуживание", callback_data="menu:requests")],

        ]
    )


def main_menu_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Список объектов", callback_data="menu:vehicles"),
            InlineKeyboardButton(text="🔧 Заявки на ремонт", callback_data="menu:requests"),
        ]
    ])
    return kb


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Кареты", callback_data="menu:vehicles"),
            InlineKeyboardButton(text="🔧 Заявки", callback_data="menu:requests"),
        ]
    ])
    return kb

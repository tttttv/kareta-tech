from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.enums import VehicleRequestStatus
from src.enums import VehicleStatusEnum
from src.keyboards.utils.nav_keyboard import MENU_BUTTON
from src.enums import VehicleStatusEnum


def vehicle_keyboard(objects):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=obj['name'], callback_data=f"vehicle:{obj['id']}")]
            for obj in objects
        ] + [MENU_BUTTON]
    )
    return kb


def vehicle_action_keyboard(vehicle_id, is_locked: bool) -> InlineKeyboardMarkup:
    lock_button = (
        InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"unlock:{vehicle_id}")
        if is_locked
        else InlineKeyboardButton(text="🔒 Заблокировать", callback_data=f"lock:{vehicle_id}")
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                lock_button,
                InlineKeyboardButton(text="На карте", callback_data=f"location:{vehicle_id}")
            ],
            [
                InlineKeyboardButton(text="📣 Сигнал", callback_data=f"beep:{vehicle_id}")
            ]
        ] + [MENU_BUTTON]
    )
    return kb


def repair_request_keyboard(objects):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Звявка №{obj["id"]}', callback_data=f"repair_req:{obj['id']}")]
            for obj in objects
        ] + [MENU_BUTTON]
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
    buttons_markup.append(MENU_BUTTON)

    return InlineKeyboardMarkup(inline_keyboard=buttons_markup)


def vehicle_status_keyboard(rep_id: int, request_status: VehicleRequestStatus) -> InlineKeyboardMarkup:
    statuses = [
        (VehicleStatusEnum.UNAVAILABLE_IN_SERVICE, "🔧 Ремонт"),
        (VehicleStatusEnum.UNAVAILABLE_IN_SERVICE, "🩸 Донор"),
        (VehicleStatusEnum.UNAVAILABLE_IN_MAINTENANCE, "🛠 Обслуживание"),
    ]
    buttons = [
        InlineKeyboardButton(
            text=label,
            callback_data=f"set_vehicle_status:{rep_id}:{request_status.value}:{status.value}"
        ) for status, label in statuses
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons] + [MENU_BUTTON])


def main_menu_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Кареты", callback_data="menu:vehicles"),
            InlineKeyboardButton(text="🔧 Заявки", callback_data="menu:requests"),
            InlineKeyboardButton(text="Найти по айди", callback_data="find_vehicle"),
        ]
    ])
    return kb

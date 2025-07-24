from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def objects_keyboard(objects):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=obj['name'], callback_data=f"select:{obj['id']}")]
            for obj in objects
        ]
    )
    return kb


def object_action_keyboard(vehicle_id):
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
                InlineKeyboardButton(text="🛠 В ремонт", callback_data=f"set_status:{vehicle_id}:В ремонте"),
                InlineKeyboardButton(text="✅ Доступен", callback_data=f"set_status:{vehicle_id}:Доступен")
            ]
        ]
    )
    return kb

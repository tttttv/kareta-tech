from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def append_navigation_keyboard(keyboard: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    """Добавляет кнопки навигации внизу клавиатуры"""
    navigation_buttons =  [
            InlineKeyboardButton(text="🚗 Кареты", callback_data="menu:vehicles"),
            InlineKeyboardButton(text="🔧 Заявки", callback_data="menu:requests"),
        ]
    keyboard.inline_keyboard.append(navigation_buttons)
    return keyboard
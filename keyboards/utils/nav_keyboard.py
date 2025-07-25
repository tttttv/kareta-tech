from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def append_navigation_keyboard(
    base_keyboard: InlineKeyboardMarkup | None = None
) -> InlineKeyboardMarkup:
    """
    Добавляет в конец клавиатуры кнопки навигации.
    Если base_keyboard не передана, возвращает клавиатуру с навигационными кнопками.
    """
    navigation_buttons = [
        InlineKeyboardButton(text="🚗 Кареты", callback_data="menu:vehicles"),
        InlineKeyboardButton(text="🔧 Заявки", callback_data="menu:requests"),
    ]

    if base_keyboard is None:
        # Создаём новую клавиатуру только с навигацией
        new_keyboard = InlineKeyboardMarkup(inline_keyboard=[navigation_buttons])
    else:
        # Копируем существующие кнопки и добавляем навигацию
        new_keyboard = InlineKeyboardMarkup(inline_keyboard=[*base_keyboard.inline_keyboard])
        new_keyboard.inline_keyboard.append(navigation_buttons)

    return new_keyboard
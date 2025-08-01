from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


MENU_BUTTON = [InlineKeyboardButton(text="В меню", callback_data="to_start")]
BACK_TO_GEOZONES = [InlineKeyboardButton(text="Назад", callback_data="geozone:")]
BACK_TO_REPAIR_REQUESTS = [InlineKeyboardButton(text="Назад", callback_data="menu:requests_by_geozone")]
BACK_TO_GEOZONE_SELECTION = [InlineKeyboardButton(text="🔙 Назад", callback_data="choose_geozone")]

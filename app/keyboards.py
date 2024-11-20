from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для настроек
settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить канал", callback_data="add_channel")],
    [InlineKeyboardButton(text="Удалить канал", callback_data="delete_channel")],
    ])
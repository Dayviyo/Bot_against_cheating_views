from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database import fetch_channels

# Клавиатура для настроек
settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Удалить канал", callback_data="delete_channel")],
    ])

async def all_channels_keyboard():
    channels = await fetch_channels()

    if not channels:
        return None

    # Создаём клавиатуру с кнопками для каждого канала
    keyboard = InlineKeyboardBuilder()
    for channel_id, channel_title in channels:
        keyboard.add(InlineKeyboardButton(text=channel_title, callback_data=f"delete_channel_{channel_id}"))

    return keyboard
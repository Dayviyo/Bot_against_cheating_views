from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.keyboards import settings_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я помогу тебе спасти пост от накрутки')


@router.message(Command('settings'))
async def settings(message: Message):
    await message.answer('Какую функцию ты хочешь использовать?', reply_markup=settings_keyboard)


@router.callback_query(F.data == "add_channel")
async def handle_add_channel(callback: CallbackQuery):
    """Обработка выбора 'Добавить канал'."""
    await callback.message.answer(
        "Чтобы добавить канал, введите данные в формате:\n"
        "`channel_id message_id max_views time_interval repost_delay`\n\n"
        "Пример: `123456789 1 500 120 60`",
        parse_mode="Markdown"
    )
    await callback.answer()  # Закрыть окно уведомления


@router.callback_query(F.data == "delete_channel")
async def handle_delete_channel(callback: CallbackQuery):
    """Обработка выбора 'Удалить канал'."""
    await callback.message.answer(
        "Чтобы удалить канал, отправьте его ID в следующем формате:\n"
        "`/delete_channel <channel_id>`\n\n"
        "Пример: `/delete_channel 123456789`",
        parse_mode="Markdown"
    )
    await callback.answer()  # Закрыть окно уведомления

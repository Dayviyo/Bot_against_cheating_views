from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database import add_or_update_channel
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
    pass


@router.callback_query(F.data == "delete_channel")
async def handle_delete_channel(callback: CallbackQuery):
    """Обработка выбора 'Удалить канал'."""
    pass


@router.channel_post()
async def handle_message(message: Message):
    """Обработка сообщений из канала и запись данных в базу."""
    print('Пришло сообщение в канал!')
    if message.chat.type == "channel":  # Проверяем, что сообщение пришло из канала
        channel_id = message.chat.id
        message_id = message.message_id
        title = message.chat.title

        # Параметры по умолчанию (можно изменить на основе пользовательских настроек)
        max_views = 200  # Лимит просмотров
        repost_delay = 60  # Задержка в секундах перед повторной публикацией
        
        # Сохраняем данные в базу
        try:
            print('Сохраняю в кнаал')
            
            await add_or_update_channel(channel_id, title, message_id, max_views, repost_delay)
        except Exception as e:
            print(f"Ошибка при добавлении в базу: {e}")
    else:
        print("Получено сообщение не из канала.")
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database import add_or_update_channel, delete_channel
from app.keyboards import settings_keyboard, all_channels_keyboard
from params import tg_username, MAX_VIEWS, REPOST_DELAY
from app.logger import main_logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я помогу тебе спасти пост от накрутки')


@router.message(Command('settings'))
async def settings(message: Message):
    if message.from_user.username in tg_username:
        await message.answer('Какую функцию ты хочешь использовать?', reply_markup=settings_keyboard)
    
    else:
        await message.answer('Вам недоступна эта функция')


@router.callback_query(F.data == "delete_channel")
async def handle_delete_channel(callback: CallbackQuery):
    """Обработка выбора 'Удалить канал'."""
    await callback.answer()  # Закрываем callback-запрос

    channels_keyboard = await all_channels_keyboard()

    if channels_keyboard is None:
        # Редактируем текст предыдущего сообщения
        await callback.message.edit_text("Нет каналов в базе данных")
        return

    # Редактируем текст и добавляем клавиатуру
    await callback.message.edit_text(
        "Выберите канал для удаления:",
        reply_markup=channels_keyboard.as_markup())


# Обработка выбора канала для удаления
@router.callback_query(F.data.startswith("delete_channel_"))
async def handle_channel_deletion(callback: CallbackQuery):
    """Удаление выбранного канала."""
    channel_id = callback.data.split("_")[-1]  # Получаем ID канала из callback_data

    try:
        await delete_channel(channel_id)
        await callback.message.edit_text(f"Канал с ID {channel_id} успешно удалён.")

    except Exception as e:
        await callback.message.edit_text(f"Ошибка при удалении канала: {e}")


@router.channel_post()
async def handle_message(message: Message):
    """Обработка сообщений из канала и запись данных в базу."""
    if message.chat.type == "channel":  # Проверяем, что сообщение пришло из канала
        channel_id = message.chat.id
        message_id = message.message_id
        title = message.chat.title
        
        # Сохраняем данные в базу
        try:
            await add_or_update_channel(channel_id, title, message_id, MAX_VIEWS, REPOST_DELAY)
            
        except Exception as e:
            main_logger.error(f"Ошибка при добавлении в базу: {e}")
    else:
        main_logger.info("Получено сообщение не из канала.")
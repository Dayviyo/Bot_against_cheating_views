import asyncio
import aiosqlite

from app.get_views_script import get_message_views
from app.database import delete_channel
from params import TIME_INTERVAL
from app.logger import main_logger

DB_PATH = "app/data.db"


async def process_channel(bot, conn, channel):
    """Обрабатывает один канал: проверяет просмотры и перезаливает сообщения при необходимости."""
    channel_id, channel_title, message_id, max_views, current_views, repost_delay = channel[1:]

    try:
        # Получаем информацию о сообщении
        message = await get_message_views(int(channel_id), int(message_id))

        # Удаляем канал, если он заблокирован
        if message == "error":
            main_logger.error(f"Канал '{channel_title}' заблокирован, удаляю из базы.")
            await delete_channel(channel_id)
            return

        # Проверяем, превысил ли пост лимит просмотров
        view_increase = message.views - current_views
        if view_increase >= max_views:
            main_logger.critical(
                f'Пост в канале "{channel_title}" превысил норму: +{view_increase} просмотров за {TIME_INTERVAL} секунд!'
            )

            # Удаляем старое сообщение
            await bot.delete_message(channel_id, message_id)

            # Ждем задержку перед повторной публикацией
            await asyncio.sleep(repost_delay)

            # Публикуем новое сообщение
            new_message = await bot.send_message(channel_id, message.text)

            # Обновляем базу данных
            await conn.execute(
                "UPDATE channels SET message_id = ?, current_views = ? WHERE channel_id = ?",
                (new_message.message_id, 1, channel_id),
            )
            await conn.commit()

            main_logger.critical(f'Пост в канале "{channel_title}" опубликован снова.')

        else:
            # Если лимит не превышен, просто обновляем просмотры
            main_logger.info(f'Просмотры канала "{channel_title}" не превысили норму.')
            await conn.execute(
                "UPDATE channels SET current_views = ? WHERE channel_id = ?",
                (current_views, channel_id),
            )
            await conn.commit()

    except Exception as e:
        main_logger.error(f"Ошибка с каналом '{channel_title}': {e}")


async def monitor_channels(bot):
    """Основной цикл мониторинга каналов."""
    while True:
        main_logger.info("Начал проверку каналов")

        # Подключение к базе данных
        async with aiosqlite.connect(DB_PATH) as conn:
            async with conn.execute("SELECT * FROM channels") as cursor:
                channels = await cursor.fetchall()

            if not channels:
                main_logger.warning("Нет каналов для мониторинга.")
                await asyncio.sleep(TIME_INTERVAL)
                continue

            # Последовательно обрабатываем каждый канал
            for channel in channels:
                await process_channel(bot, conn, channel)

        # Задержка перед следующей проверкой
        await asyncio.sleep(TIME_INTERVAL)
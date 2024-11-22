import asyncio
import aiosqlite

from app.get_views_script import get_message_views
from app.database import delete_channel
from params import TIME_INTERVAL
from app.logger import main_logger

DB_PATH = "app/data.db"

async def monitor_channels(bot):
    while True:
        main_logger.info('Начал проверку каналов')

        # Интервал времени через который будут проверяться сообщения

        async with aiosqlite.connect(DB_PATH) as conn:
            async with conn.execute("SELECT * FROM channels") as cursor:
                channels = await cursor.fetchall()

        if not channels:
            main_logger.error('Нет каналов для мониторинга')
            await asyncio.sleep(TIME_INTERVAL)
            continue

        for channel in channels:
            channel_id, channel_title, message_id, max_views, repost_delay = channel[1:]
            try:
                # Получаем информацию о сообщении
                message = await get_message_views(int(channel_id), int(message_id))

                # Удаление забаненного канала
                if message == 'error':
                    await delete_channel(channel_id)
                    continue

                # Проверяем просмотры
                if message.views > max_views:
                    main_logger.critical(f'Пост в канале "{channel_title}" превысил норму: {message.views} просмотров!')
                    
                    # Удаляем сообщение
                    await bot.delete_message(channel_id, message_id)

                    # Публикуем сообщение снова через задержку
                    await asyncio.sleep(repost_delay)
                    new_message = await bot.send_message(channel_id, message.text)

                    # Обновляем message_id в базе данных
                    async with aiosqlite.connect(DB_PATH) as conn:
                        await conn.execute(
                            "UPDATE channels SET message_id = ? WHERE channel_id = ?",
                            (new_message.message_id, channel_id)
                        )
                        await conn.commit()

                    main_logger.critical(f'Пост в канале "{channel_title}" опубликован снова')

                else:
                    main_logger.info(f'Просмотры канала "{channel_title}" не превысили норму')

            except Exception as e:
                main_logger.error(f"Ошибка с каналом '{channel_title}': {e}")

        await asyncio.sleep(TIME_INTERVAL)
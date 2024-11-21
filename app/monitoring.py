import asyncio
import aiosqlite

from app.script import get_message_views
from app.database import delete_channel

DB_PATH = "app/data.db"

async def monitor_channels(bot):
    while True:
        print('Мониторю')

        # Интервал времени через который будут проверяться сообщения
        TIME_INTERVAL = 10

        async with aiosqlite.connect(DB_PATH) as conn:
            async with conn.execute("SELECT * FROM channels") as cursor:
                channels = await cursor.fetchall()

        if not channels:
            print('Нет каналов для мониторинга')
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
                    print(f'Пост в канале "{channel_title}" превысил норму: {message.views} просмотров!')
                    
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

                    print(f'Пост в канале "{channel_title}" опубликован снова')

                else:
                    print(f'Просмотры канала "{channel_title}" не превысили норму')

            except Exception as e:
                print(f"Ошибка с каналом '{channel_title}': {e}")

        await asyncio.sleep(TIME_INTERVAL)
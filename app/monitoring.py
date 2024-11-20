import asyncio
import sqlite3

async def monitor_channels(bot):
    while True:
        print('Мониторю')
        conn = sqlite3.connect("app/data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels")
        channels = cursor.fetchall()
        conn.close()

        for channel in channels:
            channel_id, message_id, max_views, time_interval, repost_delay = channel[1:]
            try:
                # Получаем сообщение
                message = await bot.get_chat_message(channel_id, message_id)

                # Проверяем просмотры
                if message.views > max_views:
                    await bot.delete_message(channel_id, message_id)

                    # Публикуем через задержку
                    await asyncio.sleep(repost_delay)
                    await bot.send_message(channel_id, message.text)

            except Exception as e:
                print(f"Ошибка с каналом {channel_id}: {e}")
        await asyncio.sleep(10)
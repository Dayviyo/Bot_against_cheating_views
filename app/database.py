import aiosqlite
from app.logger import main_logger

DB_PATH = "app/data.db"

async def init_db():
    """Инициализация базы данных: создание таблицы channels."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL UNIQUE,
            channel_title TEXT,
            message_id INTEGER,
            max_views INTEGER NOT NULL,
            current_views INTEGER NOT NULL,
            repost_delay INTEGER NOT NULL
        )
        """)
        await conn.commit()


async def add_or_update_channel(channel_id, channel_title, message_id, max_views, current_views, repost_delay):
    """Добавление нового канала или обновление существующего."""
    
    # Проверяем, существует ли канал в базе
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT 1 FROM channels WHERE channel_id = ?", (channel_id,))
        existing_channel = await cursor.fetchone()

        if existing_channel:
            main_logger.info(f"В канал {channel_title} пришло новое сообщение. Теперь буду отслеживать его")
            await conn.execute(
                    "UPDATE channels SET message_id = ? WHERE channel_id = ?",
                    (message_id, channel_id)
                )
            await conn.commit()
            return

        # Если канал не существует, добавляем его
        await conn.execute("""
        INSERT INTO channels (channel_id, channel_title, message_id, max_views, current_views, repost_delay)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (channel_id, channel_title, message_id, max_views, current_views, repost_delay))
        await conn.commit()
        main_logger.info(f"Канал '{channel_title}' успешно добавлен в базу.")


async def delete_channel(channel_id):
    """Удаление канала из базы данных."""
    async with aiosqlite.connect(DB_PATH) as conn:
        try:
            await conn.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
            await conn.commit()

            main_logger.error(f'Канал {channel_id} успешно удален')
        except Exception as e:
            main_logger.error(f'Произошла ошибка удаление канала {channel_id}: {e}')


async def fetch_channels():
    """Получить список каналов из базы данных."""
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("SELECT channel_id, channel_title FROM channels") as cursor:
            channels = await cursor.fetchall()
    return channels
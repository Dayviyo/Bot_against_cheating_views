import aiosqlite

DB_PATH = "app/data.db"

async def init_db():
    """Инициализация базы данных: создание таблицы channels."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL UNIQUE,
            message_id INTEGER,
            max_views INTEGER NOT NULL,
            time_interval INTEGER NOT NULL,
            repost_delay INTEGER NOT NULL
        )
        """)
        await conn.commit()


async def add_or_update_channel(channel_id, message_id, max_views, time_interval, repost_delay):
    """Добавление нового канала или обновление существующего."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
        INSERT INTO channels (channel_id, message_id, max_views, time_interval, repost_delay)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(channel_id) DO UPDATE SET
            message_id=excluded.message_id,
            max_views=excluded.max_views,
            time_interval=excluded.time_interval,
            repost_delay=excluded.repost_delay
        """, (channel_id, message_id, max_views, time_interval, repost_delay))
        await conn.commit()


async def get_channel_settings(channel_id):
    """Получение настроек канала по его ID."""
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("SELECT * FROM channels WHERE channel_id = ?", (channel_id,)) as cursor:
            channel = await cursor.fetchone()
    return channel


async def delete_channel(channel_id):
    """Удаление канала из базы данных."""
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
        await conn.commit()
import aiosqlite

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
            repost_delay INTEGER NOT NULL
        )
        """)
        await conn.commit()


async def add_or_update_channel(channel_id, channel_title, message_id, max_views, repost_delay):
    """Добавление нового канала или обновление существующего."""
    
    # Проверяем, существует ли канал в базе
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT 1 FROM channels WHERE channel_id = ?", (channel_id,))
        existing_channel = await cursor.fetchone()

        if existing_channel:
            print(f"Канал с ID {channel_id} уже существует в базе. Пропускаем добавление.")
            return  # Если канал уже есть, не добавляем его снова

        # Если канал не существует, добавляем его
        await conn.execute("""
        INSERT INTO channels (channel_id, channel_title, message_id, max_views, repost_delay)
        VALUES (?, ?, ?, ?, ?)
        """, (channel_id, channel_title, message_id, max_views, repost_delay))
        await conn.commit()
        print(f"Канал {channel_title} успешно добавлен в базу.")



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
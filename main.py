from aiogram import Bot, Dispatcher
import asyncio

from app.handlers import router
from params import API_TOKEN
from app.database import init_db
from app.monitoring import monitor_channels


async def main():
    # Инициализация базы данных
    await init_db()
    
    # Создание бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Запуск мониторинга каналов как фоновой задачи
    monitoring_task = asyncio.create_task(monitor_channels(bot))
    
    try:
        await dp.start_polling(bot)
    finally:
        monitoring_task.cancel()
        await monitoring_task

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

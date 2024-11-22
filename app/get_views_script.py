from params import API_ID, API_HASH
from app.logger import main_logger

from telethon import TelegramClient
from telethon.errors import ChannelPrivateError, ChannelInvalidError, NeedChatInvalidError

api_id = API_ID
api_hash = API_HASH

client = TelegramClient('session_name', api_id, api_hash)

async def get_message_views(channel_id, message_id):
    async with client:

        try:
            message = await client.get_messages(channel_id, ids=message_id)
            if message:
                return message
            else:
                main_logger.error("Сообщение не найдено. Канал будет удален из базы данных")
                return 'error'
        
        # Проверка на существование канала
        except (ChannelPrivateError, ChannelInvalidError, NeedChatInvalidError) as e:
            main_logger.error(f"Ошибка доступа к каналу {channel_id}: {e}.\nВозможно канал удален или заблокирован")
            return 'error'
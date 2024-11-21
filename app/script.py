from params import API_ID, API_HASH

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
                print("Сообщение не найдено.")
        
        # Проверка на существование канала
        except (ChannelPrivateError, ChannelInvalidError, NeedChatInvalidError) as e:
            print(f"Ошибка доступа к каналу {channel_id}: {e}")
            return "error"
from telethon import TelegramClient, events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from dotenv import load_dotenv, dotenv_values
import platform, os, re

# load .env variables
load_dotenv()

config = dotenv_values(".env")

api_id = os.environ['api_id']
api_hash = os.environ['api_hash']
bot_token = os.environ['bot_token']
print(api_hash, api_id)
client = TelegramClient('BOT', api_id, api_hash).start(bot_token=bot_token)


rights = ChatBannedRights(
        until_date=None,
        view_messages=True,
        send_messages=False,
        send_media=False,
        send_stickers=False,
        send_gifs=False,
        send_games=False,
        send_inline=False,
        embed_links=False,
        send_polls=False,
        change_info=False,
        invite_users=False,
        pin_messages=False
    )


@client.on(events.NewMessage)
async def handle_new_message(event):
    try:
        user_info =  await client(GetFullUserRequest(event.message.from_id.user_id))
        # Check platform
        try:
            # Windows
            user_bio = user_info.about
            user_bio =  str(user_bio).lower()
        except:
            # Unix
            user_bio = user_info.full_user.about
            user_bio =  str(user_bio).lower()
    except:
        user_bio = None
    print(user_bio)
    message = str(event.message.message).lower()
    if ("http" in str(user_bio) or "https" in str(user_bio)) or ("@" in str(user_bio) and "bot" in str(user_bio) ) or 't.me' in str(user_bio):
        await client.delete_messages(event.chat_id, [event.id])
        print(user_bio)
        print(message)
        await client(functions.channels.EditBannedRequest(event.chat_id, event.message.from_id.user_id, rights))
    if ("http" in str(message) or "https" in str(message) ) or ("@" in str(message) and "bot" in str(message) ):
        print(user_bio)
        print(message)
        await client.delete_messages(event.chat_id, [event.id])
        await client(functions.channels.EditBannedRequest(event.chat_id, event.message.from_id.user_id, rights))
print(f"\nRun OS: {platform.system()}\n")
client.run_until_disconnected()
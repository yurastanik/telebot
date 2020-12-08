from telethon import TelegramClient
import sqlite3
import traceback
import sys
from threading import Timer
import time

api_id = 1197665
api_hash = '3d066cbf78e6561ad40953f4cf66f76d'
phone = '+380500279850'


async def error(client: TelegramClient):
    try:
        try:
            await client.start()
        except sqlite3.OperationalError:
            await error(client)
        return client
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        from bot import Bot
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


async def auth():
    try:
        entity = "alert"
        client = TelegramClient(entity, api_id, api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            from bot import Bot
            Bot(None).sendMessage(text="CODE - alert")
            await client.send_code_request(phone)
            await client.sign_in(phone, code=input('code: '))
        client = await error(client)
        return client
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        from bot import Bot
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


async def sheldue():
    client = await auth()
    while True:
        await client.send_message("@muspla_bot", "/start")
        time.sleep(1200)

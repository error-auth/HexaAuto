import asyncio
import re
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError

api_id = 4608923
api_hash = '0fc54e6096c9cd77cd1e1954b899676d'

async def main():
    client = TelegramClient('account4', api_id, api_hash)
    await client.start()

    print('''
          Acoount Logged in
                                 ~ paradox  ''')
    

    await client.run_until_disconnected()

asyncio.run(main())

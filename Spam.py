import asyncio
import random
from telethon import TelegramClient, events

api_id = 4608923
api_hash = '0fc54e6096c9cd77cd1e1954b899676d'

# List of session files for different accounts
session_files = ['account1.session', 'account2.session', 'account3.session', 'account4.session']

class Account:
    def __init__(self, session_file):
        self.client = TelegramClient(session_file, api_id, api_hash)
        self.stop_hunting = False

    async def start_hunting(self):
        async with self.client:
            bot_entity = await self.client.get_entity('@HeXamonbot')
            while not self.stop_hunting:
                last_messages = await self.client.get_messages(bot_entity, limit=2)
                shiny_found = any('✨ shiny pokemon found!' in message.message.lower() for message in last_messages)
                if shiny_found:
                    self.stop_hunting = True
                    print('Shiny Pokemon found in last messages!')
                    break

                for message in last_messages:
                    await self.handle_message(message)

                if not self.stop_hunting:
                    await self.client.send_message('@HeXamonbot', '/hunt')
                    gap = random.randint(2, 6)
                    await asyncio.sleep(gap)

    async def handle_message(self, message):
        stop_keywords = [
            "✨ Shiny Pokémon found!", "Daily hunt limit reached"
        ]

        if any(keyword in message.message for keyword in stop_keywords):
            self.stop_hunting = True
            print(f"Found stopping keyword in message: {message.message}")
        else:
            print(f"Received message: {message.message}")

    async def connect(self):
        await self.client.start()
        print(f"Connected client with session: {self.client.session.filename}")
        # Handle OTP and TFA code if required

    def close(self):
        self.stop_hunting = True
        self.client.disconnect()
        print(f"Disconnected client with session: {self.client.session.filename}")

async def main(session_file):
    account = Account(session_file)
    await account.connect()

    while not account.stop_hunting:
        await account.start_hunting()

    account.close()
    print(f"Script stopped for session: {session_file}")

# Run the main function for each session file
async def run_all_clients():
    tasks = []
    for session_file in session_files:
        tasks.append(main(session_file))
    await asyncio.gather(*tasks)

asyncio.run(run_all_clients())

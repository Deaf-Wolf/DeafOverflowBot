# main.py
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignoriere Nachrichten vom Bot selbst
        if message.author == self.user:
            return

        # Prüfe, ob die Nachricht mit '!' beginnt
        if message.content.startswith('!'):
            command = message.content[1:]  # Entfernt das '!'
            if command == 'hallo':
                await message.channel.send('Hallo!')

        
        # Wenn du möchtest, kannst du auch einfach alle Nachrichten anzeigen
        else:
            print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
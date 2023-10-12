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
        # Ignores messages from bot 
        if message.author == self.user:
            return

        # checks if messages contains '!'
        if message.content.startswith('!'):
            command = message.content[1:]  # Entfernt das '!'
            if command == 'hallo':
                await message.channel.send('Hallo!')
            elif command == 'help':
                help_message = """
                **Liste aller Befehle:**
                `!hallo` - Sagt Hallo!
                `!help` - Zeigt diese Hilfe an.
                """
                await message.channel.send(help_message)
        
        # prints every messages in console 
        else:
            print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)


# test commit
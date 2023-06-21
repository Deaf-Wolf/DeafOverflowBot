import discord
import os

from Skills.RollenZuweiser import RoleZuweiser

from dotenv import load_dotenv

intents = discord.Intents.all()


load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('TOKEN')
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content is None or not message.content.strip():
        return

    print(f"Received message: {message.content}")

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    elif message.content.lower().startswith('!roles'):
        print("Received !roles command")
        role_zuweiser = RoleZuweiser()
        await role_zuweiser.send_role_message(message.channel)

@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        print(f"Reaction added: {reaction.emoji} by {user.name}")
        role_zuweiser = RoleZuweiser()
        await role_zuweiser.process_reaction(reaction, user)

client.run(TOKEN)

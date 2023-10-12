# main.py
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View


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

            elif command == 'roles':
                roles = ', \n'.join([role.name for role in message.guild.roles])
                await message.channel.send(f"Dieser server hat die Rollen:\n{roles}")

                #Erstellen Sie Schaltflächen für jede Rolle
                view = View()
                for role in message.guild.roles:
                    if role.name != "@everyone":
                        view.add_item(Button(label=role.name, custom_id=str(role.id)))
                await message.channel.send("Klicken Sie auf eine Schaltfläche, um eine Rolle hinzuzufügen.", view=view)

            elif command == 'help':
                help_message = """
                **Liste aller Befehle:**
                `!hallo` - Sagt Hallo!
                `!roles` - Zeigt alle Rollen an und hügt dir Rollen hinzu :D
                `!help` - Zeigt diese Hilfe an.
                """
                await message.channel.send(help_message)
        
        # prints every messages in console 
        else:
            print(f'Message from {message.author}: {message.content}')


    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.component:
            if 'custom_id' in interaction.data and interaction.data['custom_id'].isnumeric():
                role_id = int(interaction.data['custom_id'])
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Rolle {role.name} hinzugefügt!", ephemeral=True)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = MyClient(intents=intents)
client.run(TOKEN)

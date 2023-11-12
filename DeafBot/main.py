# main.py
import discord
import os
import requests #allows usage of API
import json
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View

#Import features
from features.nasa import NASA
from features.role_handler import RoleCommandHandler



load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

#Deafoverflow Id´s
BOT_CHANNEL = int(os.getenv('BOT_CHANNEL_ID'))
WELCOME_CHANNEL = int(os.getenv('WELCOME_CHANNEL'))
#Features key´s
NASA_API_KEY = str(os.getenv('NASA_API_KEY'))

#TestServer Id´s bellow


#Loads and Reads .json file
def load_json(filename):
    with open(filename, 'r') as file:
        return set(json.load(file))    






class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = discord.utils.get(self.get_all_channels(), id=BOT_CHANNEL)
        if channel:
            await channel.send("Ich bin wach!")

            #load copyright filter list
            allowed_licenses = load_json('allowed_licenses.json')
        else:
            print(f"Kanal mit ID {BOT_CHANNEL} nicht gefunden!")

    #New Member Joins
    async def on_member_join(self, member):
        welcome_channel = discord.utils.get(self.get_all_channels(), id=WELCOME_CHANNEL)
        if welcome_channel:
            await welcome_channel.send(f'Willkommen auf dem Server, {member.mention}!')
        else:
            print(f"Kanal 'willkommenskanal' nicht gefunden!")


    async def on_message(self, message):
        # Ignores messages from bot 
        if message.author == self.user:
            return

        # checks if messages contains '!'
        if message.content.startswith('!'):
            command = message.content[1:]  # Removes the '!'
            if command == 'hallo':
                await message.channel.send('Hallo!')

            #Show list of commands
            elif command == 'help':
                help_message = """
                **Liste aller Befehle:**
                `!help` - Zeigt diese Hilfe an.
                `!hallo` - Sagt Hallo!
                `!roles` - Zeigt alle Rollen an und hügt dir Rollen hinzu :D
                `!removeRoles` - Entfernt deine Rollen
                `!apod` - Zeigt NASA Bild des Tages an <3
                """
                await message.channel.send(help_message)

            #Show and add Roles
            elif command == 'roles':
                await RoleCommandHandler.show_roles(message)

            #Show and remove user Roles
            elif command == 'removeRoles':
               await RoleCommandHandler.remove_roles(message)

            #Respons with Nasa APOD Pic of the Day
            elif command == 'apod':
                ## await NASA.get_apod(message , NASA_API_KEY)
                await message.channel.send("Sorry, APOD is Locked.")
               
      
        # prints every messages in console 
        else:
            print(f'Message from {message.author}: {message.content}')


    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.component:
            if 'custom_id' in interaction.data:
                custom_id = interaction.data['custom_id']
                
                # !roles
                if custom_id.startswith('add_'):
                    role_id = int(custom_id[4:])
                    role = discord.utils.get(interaction.guild.roles, id=role_id)
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"Rolle {role.name} hinzugefügt!", ephemeral=True)
                
                # !removeRoles
                elif custom_id.startswith('remove_'):
                    role_id = int(custom_id[7:])
                    role = discord.utils.get(interaction.guild.roles, id=role_id)
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message(f"Rolle {role.name} entfernt!", ephemeral=True)
    


    #if bot stops running 
    async def close(self):
            await channel.send("Ich gehe schlafen!")
            channel = discord.utils.get(self.get_all_channels(), id=BOT_CHANNEL)
            await super().close()                                    

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)

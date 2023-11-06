# main.py
import discord
import os
import requests #allows usage of API
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

#Deafoverflow Id´s
BOT_CHANNEL = os.getenv('BOT_CHANNEL_ID')
WELCOME_CHANNEL = os.getenv('WELCOME_CHANNEL')
#TestServer Id´s bellow

# Gets the Picture of NASA A Picture Of the Day
def get_apod():
    api_key = os.getenv('NASA_API_KEY')
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    
    # Check if request was successfull 
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error when Get APOD Picture.")
        return None


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = discord.utils.get(self.get_all_channels(), id=BOT_CHANNEL)
        if channel:
            await channel.send("Ich bin wach!")
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

            #Show and add Roles
            elif command == 'roles':
                #List all roles of the server
                roles = ', \n'.join([role.name for role in message.guild.roles if role.name != "@everyone" and role.name != "DeafBot"])
                await message.channel.send(f"Dieser server hat die Rollen:\n{roles}")

                #Creates a button for each role
                view = View()
                server_roles = [role for role in message.guild.roles if role.name != "@everyone" and role.name != "DeafBot"]
                #Checks if Server has Roles
                if not server_roles:
                    await message.channel.send(f"Keine Rollen zum Hinzufügen!")
                else:
                    for role in server_roles:
                        view.add_item(Button(label=role.name, custom_id=f"add_{role.id}"))
                    await message.channel.send("Klicken Sie auf eine Schaltfläche, um eine Rolle hinzuzufügen.", view=view)

            #Show and remove user Roles
            elif command == 'removeRoles':
                #List roles of the user
                roles = ', \n'.join([role.name for role in message.author.roles if role.name != "@everyone" and role.name != "DeafBot"])
                await message.channel.send(f"{message.author.name} hat die Rollen:\n{roles}")

                #Creates a button for each role
                view = View()
                user_roles = [role for role in message.author.roles if role.name != "@everyone" and role.name != "DeafBot"]

                #Checks if user has a role or not
                if not user_roles:
                    await message.channel.send(f"{message.author.name} hat keine Rollen HHAHAHAHA")
                else:
                    for role in user_roles:
                        view.add_item(Button(label=f"Entferne {role.name}", custom_id=f"remove_{role.id}"))
                    await message.channel.send("Klicken Sie auf eine Schaltfläche, um eine Rolle zu entfernen.", view=view)

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

            #Respons with Nasa APOD Pic of the Day
            elif command == 'apod':
                apod_data = get_apod()
                if apod_data:
                    title = apod_data['title']
                    explanation = apod_data['explanation']
                    url = apod_data['url']
                    
                    # Returns Message to Channel 
                    await message.channel.send(f"**{title}**\n{explanation}\n{url}")

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
            channel = discord.utils.get(self.get_all_channels(), id=BOT_CHANNEL)
            await channel.send("Ich gehe schlafen!")
            await super().close()                                    

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)

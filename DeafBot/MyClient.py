import discord
import os
from dotenv import load_dotenv
from plugins.nasa import NASA
from plugins.jokes import Jokes

class MyClient(discord.Client):
    # Specify the directory containing the env file
    dotenv_path = 'env'
    load_dotenv(dotenv_path)
    
    #plugins key´s
    NASA_API_KEY = str(os.getenv('NASA_API_KEY'))
    
    #Deafoverflow Id´s
    BOT_CHANNEL = str(os.getenv('BOT_CHANNEL_ID'))
    WELCOME_CHANNEL = str(os.getenv('WELCOME_CHANNEL'))
    # Print values after loading from environment variables
    print(f'BOT_CHANNEL_ID: {os.getenv("BOT_CHANNEL_ID")}')
    print(f'WELCOME_CHANNEL: {os.getenv("WELCOME_CHANNEL")}')

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = discord.utils.get(self.get_all_channels(), id=int(self.BOT_CHANNEL))
        if channel:
            # await channel.send("Ich bin wach!")
            logging.info("Ich bin wach!")

            #load copyright filter list
            allowed_licenses = load_json('allowed_licenses.json')
        else:
            print(f"Kanal mit ID {self.BOT_CHANNEL} nicht gefunden!")

    #New Member Joins
    async def on_member_join(self, member):
        welcome_channel = discord.utils.get(self.get_all_channels(), id=self.WELCOME_CHANNEL)
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
                `!joke` - Outputs a Joke
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
                await NASA.get_apod(message , NASA_API_KEY)
                await message.channel.send("Sorry, APOD is Locked.")
            elif command == 'joke':
                ## Output Joke
                await Jokes.get_joke(message)
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
        channel = discord.utils.get(self.get_all_channels(), id=self.BOT_CHANNEL)
        if channel:
           # await channel.send("Ich gehe schlafen!")
           await logging.info("Ich gehe schlafen!")
        await super().close()

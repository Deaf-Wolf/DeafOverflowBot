import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()

load_dotenv()  # Load environment variables from .env file
DISCORD_TOKEN = os.getenv('TOKEN')
SERVER_ID = 1033011746614542507


bot = commands.Bot(command_prefix = "!", intents = intents)


async def dm_about_roles(member):
    print(f"DMing {member.name}...")

    await member.send(
        f"""Hi {member.name}, welcome to {member.guild.name}! 
        
            Welche Sprache benutzt du?:
                    
            * Python ()
            * JavaScript ()
            * Java
            * Rust ()
            * C# ()
            * C++ ()
            
            Was pass zu dir?:
            * azubi
            * hobby
            * freelance
            * web-entwickler
                    
            Antworte auf diese Nachricht mit deine gewünschte Rolle.

            Antworte mit die Rolle die du Löschen willst.
            """
    )

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discordserver !")

@bot.event
async def on_member_join(member):
    await dm_about_roles(member)

async def assign_roles(message):
    print("Assigning roles...")
    
    languages = set(re.findall("python|javascript|java|rust|c#|c\+\+|azubi|hobby|freelance|web-entwickler", message.content, re.IGNORECASE))


    if languages:
        server = bot.get_guild(SERVER_ID)
        
        # <-- RENAMED VARIABLE + LIST CHANGED TO SET
        new_roles = set([discord.utils.get(server.roles, name=language.lower()) for language in languages]) 

        member = await server.fetch_member(message.author.id)

        # NEW CODE BELOW
        current_roles = set(member.roles)

        roles_to_add = new_roles.difference(current_roles)
        roles_to_remove = new_roles.intersection(current_roles)


        try:
            await member.add_roles(*roles_to_add, reason="Roles assigned by WelcomeBot.")
            await member.remove_roles(*roles_to_remove, reason="Roles revoked by WelcomeBot.")
        except Exception as e:
            print(e)
            await message.channel.send("Error assigning/removing roles.")
        else:
            if roles_to_add:
                    await message.channel.send(f"Du bekommst die folgende Rolle {'s' if len(roles_to_add) > 1 else ''} auf {server.name}: { ', '.join([role.name for role in roles_to_add]) }")
                    
            if roles_to_remove:
                await message.channel.send(f"Du hast die folgende Rolle verloren{'s' if len(roles_to_remove) > 1 else ''} auf {server.name}: { ', '.join([role.name for role in roles_to_remove]) }")

    else:
        await message.channel.send("Für deine Sprache gibst noch keine Rollen, schreib eine DM an dem ADMIN.")


@bot.event
async def on_message(message):
    print("Saw a message...")
    
    if message.author == bot.user:
        return # prevent responding to self

    # NEW CODE BELOW
    # Assign roles from DM
    if isinstance(message.channel, discord.channel.DMChannel):
        await assign_roles(message)
        return
    # NEW CODE ABOVE

    # Respond to commands
    if message.content.startswith("!roles"):
        await dm_about_roles(message.author)
    elif message.content.startswith("!serverid"):
        await message.channel.send(message.channel.guild.id)
      
bot.run(DISCORD_TOKEN)
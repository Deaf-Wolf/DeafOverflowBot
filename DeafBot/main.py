import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()

load_dotenv()  # Load environment variables from .env file
DISCORD_TOKEN = os.getenv('TOKEN')
SERVER_ID = 1115994137934692402


bot = commands.Bot(command_prefix = "!", intents = intents)


async def dm_about_roles(member):
    print(f"DMing {member.name}...")

    await member.send(
        f"""Hi {member.name}, welcome to {member.guild.name}! 
        
            Which of these languages do you use:
                    
            * Python (🐍)
            * JavaScript (🕸️)
            * Rust (🦀)
            * Go (🐹)
            * C++ (🐉)
                    
            Reply to this message with one or more of the language names or emojis above so I can assign you the right roles on our server.

            Reply with the name or emoji of a language you're currently using and want to stop and I'll remove that role for you.
            """
    )

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_member_join(member):
    await dm_about_roles(member)

async def assign_roles(message):
    print("Assigning roles...")
    
    languages = set(re.findall("python|javascript|rust|go|c\+\+", message.content, re.IGNORECASE))

    language_emojis = set(re.findall("\U0001F40D|\U0001F578|\U0001F980|\U0001F439|\U0001F409", message.content))
    # https://unicode.org/emoji/charts/full-emoji-list.html

    # Convert emojis to names
    for emoji in language_emojis:
        { 
            "\U0001F40D": lambda: languages.add("python"),
            "\U0001F578": lambda: languages.add("javascript"),
            "\U0001F980": lambda: languages.add("rust"),
            "\U0001F439": lambda: languages.add("go"),
            "\U0001F409": lambda: languages.add("c++")
        }[emoji]()

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
                    await message.channel.send(f"You've been assigned the following role{'s' if len(roles_to_add) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_add]) }")
                    
            if roles_to_remove:
                await message.channel.send(f"You've lost the following role{'s' if len(roles_to_remove) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_remove]) }")

    else:
        await message.channel.send("No supported languages were found in your message.")


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
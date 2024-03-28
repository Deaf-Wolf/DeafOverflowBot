import discord
import os
import logging
from config.logConfig import logging_config
from dotenv import load_dotenv
from MyClient import MyClient

class Main:

    def __init__(self):
        # Load environment variables from .env file (more secure)
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        logging.basicConfig(**logging_config)

        # Get DISCORD_TOKEN securely from environment variable
        self.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN') #Replace Token directly on pi (Pi has no env)
        if not self.DISCORD_TOKEN:
            raise ValueError("[main] DISCORD_TOKEN not found in .env file!")

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        self.client = MyClient(intents=intents)

        # Error handling for client.run() using try-except block
        try:
            self.client.run(self.DISCORD_TOKEN)
        except discord.DiscordException as e:
            logging.error(f"Error running the bot: {e}")
            # Handle the error gracefully (e.g., restart, notify developer)

if __name__ == '__main__':
    Main()

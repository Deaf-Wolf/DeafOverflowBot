# main.py
import discord
import os
import requests #allows usage of API
import json
import logging
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
from MyClient import MyClient
#Import plugins
from plugins.role_handler import RoleCommandHandler

class Main:
    # Setting up Logging 
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    
    # Specify the directory containing the env file
    dotenv_path = 'env'
    load_dotenv(dotenv_path)
    
    DISCORD_TOKEN = str(os.getenv('DISCORD_TOKEN'))
    print(f'DISCORD_TOKEN: {DISCORD_TOKEN}')
    
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    
    client = MyClient(intents=intents)
    # For debug logging set log_level to logging.DEBUG
    client.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.INFO)
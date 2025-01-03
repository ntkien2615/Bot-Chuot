import discord
from discord.ext import commands
import os
import keep_alive
import asyncio
from dotenv import load_dotenv, find_dotenv
import random

keep_alive.awake(
    "https://bot-chuot-uw6x.onrender.com",
    debug=False)

intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='+',
                   intents=intents,
                   help_command=None,
                   case_insensitive=True)

def random_file_read(file_path):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        if lines:
            return random.choice(lines).strip()
    except (IndexError, FileNotFoundError) as e:
        return None

async def load():
    directories = [
        './commands/non-slash',
        './commands/fun',
        './commands/slash',
        './commands/general',
        './status',
        './message'
    ]
    
    for directory in directories:
        files = [f for f in os.listdir(directory) if f.endswith('.py')]
        random.shuffle(files)
        for filename in files:
            await bot.load_extension(f'{directory.replace("./", "").replace("/", ".")}.{filename[:-3]}')

async def main():
    await load()
    load_dotenv(find_dotenv())
    discord_token = os.getenv("discord_token")
    await bot.start(discord_token)


asyncio.run(main())

import discord
from discord.ext import commands
import os
import keep_alive
import asyncio
from dotenv import load_dotenv, find_dotenv

keep_alive.awake(
    "https://bot-chuot.onrender.com",
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


async def load():
    for filename in os.listdir('./commands/non-slash'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.non-slash.{filename[:-3]}')

    for filename in os.listdir('./commands/games'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.games.{filename[:-3]}')

    for filename in os.listdir('./commands/slash'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.slash.{filename[:-3]}')

    for filename in os.listdir('./commands/general'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.general.{filename[:-3]}')

    for filename in os.listdir('./status'):
        if filename.endswith('.py'):
            await bot.load_extension(f'status.{filename[:-3]}')

    for filename in os.listdir('./message'):
        if filename.endswith('.py'):
            await bot.load_extension(f'message.{filename[:-3]}')

async def main():
    await load()
    load_dotenv(find_dotenv())
    discord_token = os.getenv(discord_token)
    await bot.start(discord_token)


asyncio.run(main())

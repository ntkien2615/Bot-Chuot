import discord
from discord.ext import commands,tasks
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

# Remove the first instantiation of discord.Client
# bot = discord.Client(intents=intents)

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

def file_read_with_line(file_path, line):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        if lines:
            return lines[line].strip()
    except (IndexError, FileNotFoundError) as e:
        return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@tasks.loop(minutes=3)
async def background_task():
    channel = bot.get_channel(1077151202040614988)
    if channel:
        await channel.send("I'm still alive")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Try again in {error.retry_after:.2f} seconds.')
    else:
        raise error

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

if __name__ == "__main__":
    asyncio.run(main())